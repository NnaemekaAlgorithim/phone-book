import json
from django.http import JsonResponse
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.response import Response


class APIResponseMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Skip processing for redirect responses (300–399)
        if 300 <= response.status_code < 400:
            return response
        
        # Skip processing for certain endpoints that should return raw responses
        skip_paths = [
            '/static/',  # Static files
            '/admin/',   # Django admin
            '/api/schema/',  # API schema
            '/',  # Root ReDoc documentation
        ]
        
        # Skip processing for documentation endpoints and static content
        if any(request.path.startswith(path) for path in skip_paths):
            return response
        
        # Skip processing for HTML responses (likely documentation)
        content_type = response.get('Content-Type', '')
        if content_type.startswith('text/html') or content_type.startswith('application/json') and 'redoc' in request.path.lower():
            return response

        # Handle DRF Response objects
        if isinstance(response, Response):
            # DRF responses already have proper structure, just standardize format
            try:
                data = response.data
                
                # If it's already in our standard format, return as is
                if isinstance(data, dict) and "response_status" in data:
                    return response
                
                # Standardize DRF response
                standardized_data = {
                    "response_status": "success" if response.status_code < 400 else "error",
                    "response_description": self._get_response_description(response, data),
                    "response_data": data
                }
                
                # Create new JsonResponse with standardized format
                return JsonResponse(standardized_data, status=response.status_code)
                
            except Exception:
                # If we can't process the DRF response, return it as is
                return response

        # Handle permission errors (403)
        if response.status_code == 403:
            try:
                content = json.loads(response.content) if response.content else {}
                detail = content.get('detail', response.reason_phrase)
            except json.JSONDecodeError:
                detail = response.reason_phrase
            return JsonResponse({
                "response_status": "error",
                "response_description": f"Forbidden: {detail}",
                "response_data": {"detail": detail}
            }, status=403)

        # Handle validation errors (400)
        if response.status_code == 400:
            try:
                content = json.loads(response.content) if response.content else {}
                detail = content.get('detail', content)
            except json.JSONDecodeError:
                detail = response.reason_phrase
            return JsonResponse({
                "response_status": "error",
                "response_description": "Validation error occurred.",
                "response_data": detail
            }, status=400)

        # Handle authentication errors (401)
        if response.status_code == 401:
            try:
                content = json.loads(response.content) if response.content else {}
                detail = content.get('detail', 'Authentication credentials were not provided.')
            except json.JSONDecodeError:
                detail = 'Authentication credentials were not provided.'
            return JsonResponse({
                "response_status": "error",
                "response_description": f"Authentication required: {detail}",
                "response_data": {"detail": detail}
            }, status=401)

        # Check if the response is already a JsonResponse
        if isinstance(response, JsonResponse):
            try:
                content = json.loads(response.content)
                # Add standard fields if not already present
                if "response_status" not in content:
                    standardized_response = {
                        "response_status": "success" if response.status_code <= 399 else "error",
                        "response_description": content.get("message", "Request processed"),
                        "response_data": content.get("data", content)
                    }
                    return JsonResponse(standardized_response, status=response.status_code)
            except json.JSONDecodeError:
                pass

        # Handle other error responses
        if response.status_code > 399:
            return JsonResponse({
                "response_status": "error",
                "response_description": response.reason_phrase,
                "response_data": {}
            }, status=response.status_code)

        return response
    
    def _get_response_description(self, response, data):
        """
        Get an appropriate response description based on the response data and status code.
        """
        # Check if data has a message field
        if isinstance(data, dict):
            if 'message' in data:
                return data['message']
            elif 'detail' in data:
                return data['detail']
        
        # Default messages based on status code
        if response.status_code == 200:
            return "Request processed successfully."
        elif response.status_code == 201:
            return "Resource created successfully."
        elif response.status_code == 204:
            return "Resource deleted successfully."
        elif response.status_code == 400:
            return "Bad request."
        elif response.status_code == 404:
            return "Resource not found."
        elif response.status_code == 500:
            return "Internal server error."
        else:
            return "Request processed."
