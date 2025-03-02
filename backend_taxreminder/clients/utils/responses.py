from rest_framework import status
from rest_framework.response import Response

def format_response(data=None, message=None, status_code=status.HTTP_200_OK, errors=None, success=True):
    """
    Formats the response to follow a standard REST API structure, including a success flag.
    """
    response_data = {
        'success': success  # Include success flag to indicate request success/failure
    }

    if errors:
        response_data['errors'] = errors
    elif data:
        response_data['data'] = data
    
    if message:
        response_data['message'] = message

    return Response(response_data, status=status_code)

