from fastapi import Request, HTTPException, status
import logging
import json
import httpx


def get_bearer_token(request: Request) -> str:
    """Extracts and validates the bearer token from the request headers."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid token"
        )
    return auth_header.split("Bearer ")[1]

async def send_request(
    method: str,
    endpoint: str,
    token: str,
    payload: dict,
    client: httpx.AsyncClient
) -> dict:
    """Sends a POST request to the given endpoint with proper headers and error handling."""
    headers = {"Authorization": f"Bearer {token}"}
    method = method.upper()
    
    if method == "GET":
        response = await client.get(endpoint, params=payload, headers=headers)
    elif method == "POST":
        response = await client.post(endpoint, json=payload, headers=headers)
    elif method == "PUT":
        response = await client.put(endpoint, json=payload, headers=headers)
    elif method == "DELETE":
        response = await client.delete(endpoint, json=payload, headers=headers)
    else:
        raise ValueError(f"Unsupported HTTP method: {method}")

    logging.debug(f"Request to {endpoint} returned status: {response.status_code}")
    logging.debug(f"Response text: {response.text}")

    if response.status_code in {200, 201}:
        try:
            return response.json()
        except json.JSONDecodeError as e:
            logging.error(f"JSON decoding error: {e}")
            raise HTTPException(
                status_code=response.status_code,
                detail="Invalid JSON response from the service"
            )

    # For error responses, try to extract a JSON detail message.
    try:
        error_data = response.json()
        detail = error_data.get("detail", "Authorization failed")
    except json.JSONDecodeError:
        # Fallback to the raw text or a default message if the body is empty or not valid JSON.
        detail = response.text or "Authorization failed"

    logging.error(f"Error from authentication service: {detail}")
    raise HTTPException(status_code=response.status_code, detail=detail)

# Dependency that provides a single AsyncClient instance per request.
async def get_async_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client