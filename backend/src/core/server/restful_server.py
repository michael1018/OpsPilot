# core/server/restful_server.py
from sanic import Sanic
from sanic.request import Request
from sanic.response import json as sanic_json, text as sanic_text
from sanic.exceptions import NotFound, InvalidUsage
import asyncio
import platform
import inspect

from sanic_cors import CORS

app = Sanic("OpsPilotAPI")
# Enable CORS for all routes
CORS(app, automatic_options=True)
is_stopped = False


def parse_body(request: Request) -> dict:
    """
    Unified JSON body parser.

    - Body must exist
    - Body must be valid JSON
    - Body must be a JSON object (dict)
    """
    if not request.body:
        raise InvalidUsage("Request body is required")

    try:
        body = request.json
    except Exception:
        raise InvalidUsage("Invalid JSON body")

    if not isinstance(body, dict):
        raise InvalidUsage("JSON body must be an object")

    return body


class RESTFulApiServer:
    @staticmethod
    def run_api_server(
        host: str = "0.0.0.0",
        port: int = 7000,
        route: str = "/api",
        workers: int = 1,
        api_core=None,
    ):
        if api_core is None:
            raise ValueError("api_core must be provided")

        @app.middleware("request")
        async def attach_context(request: Request):
            """
            Attach api_core into request context
            """
            request.ctx.api_core = api_core

        @app.exception(NotFound)
        async def ignore_404s(_, __):
            """
            Handle unknown routes
            """
            return sanic_text("404 not found")

        @app.route(f"{route}/<api_name:path>", methods={"GET", "POST", "PUT", "DELETE"})
        async def api_gateway(request: Request, api_name: str):
            """
            Central API gateway:
            - Resolve API function
            - Parse parameters
            - Inject body / query parameters
            - Call endpoint function
            """
            descriptor = api_core.get_registry().get(api_name)
            if not descriptor:
                return sanic_text(
                    f"API {api_name} with method {request.method} not found",
                    status=404,
                )

            # Fault tolerance: ensure function exists
            func = descriptor.get("func")
            if func is None or not callable(func):
                return sanic_text(
                    f"API {api_name} has no callable function registered",
                    status=500,
                )

            sig = inspect.signature(func)
            call_args = {}

            # -------------------------------
            # Unified parameter injection logic
            # -------------------------------
            for name, param in sig.parameters.items():

                # Body injection rule
                if name == "body":
                    if request.method not in ("POST", "PUT", "PATCH", "DELETE"):
                        raise InvalidUsage("Request body not allowed for this method")

                    call_args[name] = parse_body(request)
                    continue

                # Query string parameters
                if name in request.args:
                    val = request.args.get(name)

                    # Type casting based on annotation
                    if param.annotation in (int, float, bool):
                        try:
                            val = param.annotation(val)
                        except Exception:
                            raise InvalidUsage(
                                f"Invalid value for parameter '{name}'"
                            )

                    call_args[name] = val
                    continue

                # Use default value if provided
                if param.default is not inspect._empty:
                    call_args[name] = param.default
                    continue

                # Missing required parameter
                raise InvalidUsage(f"Missing required parameter: {name}")

            # -------------------------------
            # Call endpoint function
            # -------------------------------
            if asyncio.iscoroutinefunction(func):
                result = await func(**call_args)
            else:
                result = func(**call_args)

            return sanic_json(result)

        @app.route("/__check")
        async def health(_):
            """
            Health check endpoint
            """
            return sanic_text("STOP" if is_stopped else "OK")

        print(f"Starting OpsPilot API server at http://{host}:{port} ...")
        if platform.system() == "Windows":
            app.run(host=host, port=port, workers=1, single_process=True)
        else:
            app.run(host=host, port=port, workers=workers)
