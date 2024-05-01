from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from functions_jwt import validate_token


class VerifyTokenRoute(APIRoute):
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            full_token = request.headers.get("Authorization")
            if not full_token:
                return JSONResponse(
                    content={"error": "Mandatory token is not present"},
                    status_code=status.HTTP_401_UNAUTHORIZED,
                )

            token = full_token.split(" ")[1]

            validation_response = validate_token(token, output=False)
            if validation_response == None:
                return await original_route(request)
            else:
                return validation_response

        return verify_token_middleware
