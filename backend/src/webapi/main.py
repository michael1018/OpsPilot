# webapi/main.py
"""
OpsPilot Web API Entry
----------------------
Directly loads API modules and starts RESTful server.
"""

import traceback
from core.server.restful_server import RESTFulApiServer
from core.api.api_core import ApiCore
from core.api.api import Api

# Import API modules so that their decorators register endpoints
import webapi.hello_api
import webapi.users_api
import webapi.auth_api

def main():
    try:
        # Get the singleton Api instance
        api_instance = Api.get_instance()
        api_core = api_instance._api_core

        # Debug: print registered APIs
        print("Registered APIs:", api_core.get_registry().keys())

        # Run RESTful server
        RESTFulApiServer.run_api_server(
            port=7000,
            api_core=api_core
        )
    except KeyboardInterrupt:
        print("Server stopped by user.")
    except Exception as e:
        traceback.print_exc()
        print("Error:", e)

if __name__ == "__main__":
    main()
