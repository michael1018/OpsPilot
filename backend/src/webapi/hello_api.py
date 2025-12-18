# webapi/hello_api.py

from core.api.api import Api

# Get the singleton Api instance
api = Api.get_instance()

# Example GET endpoint
@api.get("hello")
async def hello_endpoint(data=None):
    """
    A simple hello API endpoint.
    """
    return {"message": "Hello, OpsPilot!"}

# Example POST endpoint
@api.post("hello_post")
async def hello_post_endpoint(data=None):
    """
    A simple POST endpoint.
    """
    name = data.get("name") if data else "Guest"
    return {"message": f"Hello, {name}!"}
