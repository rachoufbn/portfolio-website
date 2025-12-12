from flask import request, g
from . import api_bp
from .exceptions import UserFacingError
from .services.file_upload import FileUploadService
from .services.repository.meetings import MeetingsService
from .services.chat import ChatService
import traceback
from datetime import datetime

def api_response_formatter(success: bool, data, status_code: int = 200):
    """The default response format for all api requests"""
    return {"success": success, "data": data}, status_code

def get_request_data():
    """Helper to get data from request (query params, JSON, or form data)"""

    # For GET/DELETE requests, use query parameters
    if request.method in ['GET', 'DELETE']:
        return request.args
    
    # For POST/PUT/PATCH, check Content-Type header to determine body format
    content_type = request.content_type or ''
    
    if 'application/json' in content_type:
        return request.get_json()
    elif 'multipart/form-data' in content_type or 'application/x-www-form-urlencoded' in content_type:
        return request.form
    
    raise UserFacingError("Unsupported Content-Type", 400)

def filter_response_fields(data, allowed_fields):
    """Filter response data to only include allowed fields"""
    if not allowed_fields:
        return data
    
    if isinstance(data, list):
        return [filter_dict(item, allowed_fields) for item in data]
    elif isinstance(data, dict):
        return filter_dict(data, allowed_fields)
    else:
        return data

def filter_dict(data, allowed_fields):
    """Filter a dictionary to only include allowed fields"""
    return {key: value for key, value in data.items() if key in allowed_fields}

@api_bp.errorhandler(UserFacingError)
def handle_user_error(e):
    """Handle user-facing errors - return the actual message"""
    return api_response_formatter(
        success = False,
        data = e.message,
        status_code = e.status_code
    )

@api_bp.errorhandler(Exception)
def handle_generic_error(e):
    """Handle all other exceptions - hide details"""

    # Log the full error for debugging
    print(f"Internal error: {traceback.format_exc()}")
    
    return api_response_formatter(
        success = False,
        data = "An internal server error has occurred",
        status_code = 500
    )

@api_bp.route("/<path:invalid_path>", methods=['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def catch_all(invalid_path):
    raise UserFacingError("Error 404: Not Found", 404)

@api_bp.route("/auth/signup", methods=['POST'])
def signup_endpoint():

    request_data = get_request_data()

    user_data = g.auth_service.signup(
        request_data['name'],
        request_data['email'],
        request_data['password']
    )

    return api_response_formatter(success=True, data=user_data)

@api_bp.route("/auth/login", methods=['POST'])
def login_endpoint():

    request_data = get_request_data()

    user_data = g.auth_service.login(
        request_data['email'],
        request_data['password']
    )

    return api_response_formatter(success=True, data=user_data)

@api_bp.route("/auth/logout", methods=['POST'])
def logout_endpoint():

    g.auth_service.logout()

    return api_response_formatter(success=True, data="Logged out successfully")

@api_bp.route("/auth/me", methods=['GET', 'PATCH'])
def current_user_endpoint():

    if not g.auth_service.is_logged_in():
        raise UserFacingError("Error 401: Unauthorized", 401)

    match request.method:
        case "GET":
            
            user_data = g.auth_service.get_client_side_user_data()
            return api_response_formatter(success=True, data=user_data)
        
        case "PATCH":

            request_data = get_request_data()
            
            updated_user_data = g.auth_service.update_user(
                request_data.get('name'),
                request_data.get('default_prompt')
            )
            
            return api_response_formatter(success=True, data=updated_user_data)

        case _:
            raise UserFacingError("Error 405: Method Not Allowed", 405)
    

@api_bp.route("/meetings", methods=['POST', 'GET'])
@api_bp.route("/meetings/<int:meeting_id>", methods=['GET', 'DELETE'])
def meetings_endpoint(meeting_id=None):
    
    user_id = g.auth_service.get_user_id()

    if user_id is None:
        raise UserFacingError("Error 401: Unauthorized", 401)

    request_data = get_request_data()

    meetings_service = MeetingsService(g.database, user_id)

    if(request.method == 'GET'):

        # Optional meeting ID to get a specific meeting
        fields = request_data.get('fields')

        meetings = meetings_service.get(meeting_id)
        meetings = filter_response_fields(meetings, fields)

        return api_response_formatter(success=True, data=meetings)

    elif(request.method == 'POST'):

        file_upload_service = FileUploadService()
        transcript = file_upload_service.handleFileUpload(
            request.files,
            file_key='transcriptFile',
            allowed_extensions={"vtt"},
            allowed_mime_types={"text/vtt", "text/plain"}, # some browsers report text/plain for .vtt
            max_size_bytes=(10 * 1024 * 1024) # 10 MB limit
        )
    
        meeting_title = request_data.get('title')
        meeting_date_time = request_data.get('timestamp')

        try:
            meeting_timestamp = datetime.fromisoformat(meeting_date_time.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            raise UserFacingError("Invalid meeting date", 400)

        meeting_id = meetings_service.create(
            title=meeting_title,
            timestamp=meeting_timestamp,
            transcript=transcript
        )

        return api_response_formatter(success=True, data={"id": meeting_id})

    elif(request.method == 'DELETE'):

        if not meetings_service.user_has_meeting(meeting_id):
            raise UserFacingError("Meeting not found", 404)

        meetings_service.delete(meeting_id)

        return api_response_formatter(success=True, data="Success")

    else:
        raise UserFacingError("Error 405: Method Not Allowed", 405)

    
