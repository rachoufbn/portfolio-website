from ..exceptions import UserFacingError

class FileUploadService:

    def handleFileUpload(self, request_files, file_key: str, allowed_extensions: set, allowed_mime_types: set, max_size_bytes: int = None) -> str:
        """Handle file upload from request"""
        
         # Validate field presence
        if file_key not in request_files:
            raise UserFacingError("No file provided", 400)

        file = request_files[file_key]
        file_name = file.filename

        # Validate file presence
        if file_name == '':
            raise UserFacingError("No file selected", 400)
        
        self._verify_file_size(file, max_size_bytes)
        
        self._verify_file_extension(file_name, allowed_extensions)
        self._verify_file_mime_type(file, allowed_mime_types)
        
        file_contents = file.read().decode('utf-8')

        return file_contents
    
    def _verify_file_extension(self, file_name, allowed_extensions: set) -> None:
        """Verify that the uploaded file has an allowed extension"""

        if '.' not in file_name:
            raise UserFacingError("File must have an extension", 400)

        file_extension = file_name.rsplit('.', 1)[1].lower()

        if file_extension not in allowed_extensions:
            allowed_ext_display = ', '.join(allowed_extensions)
            raise UserFacingError(f"Invalid file type. Only {allowed_ext_display} are supported", 400)
    
    def _verify_file_mime_type(self, file, allowed_mime_types: set) -> None:    
        """Verify that the uploaded file has an allowed MIME type"""
        
        mimetype = (file.mimetype or "").lower()
        if mimetype and mimetype not in allowed_mime_types:
            allowed_mime_display = ', '.join(allowed_mime_types)
            raise UserFacingError(f"Invalid file MIME type. Only {allowed_mime_display} is supported", 400)
    
    def _verify_file_size(self, file, max_size_bytes: int) -> None:
        """Verify that the uploaded file does not exceed the maximum size"""
        
        if max_size_bytes is not None:

            # Try to get size from content_length first
            size = getattr(file, 'content_length', None)

            if size is None:
                # Backup method to determine size
                try:
                    current_pos = file.stream.tell()
                    file.stream.seek(0, 2)
                    size = file.stream.tell()
                    file.stream.seek(current_pos)
                except Exception:
                    size = None
                
            if size is not None and size > max_size_bytes:
                max_size_mb = max_size_bytes / (1024 * 1024)
                raise UserFacingError(f"Filesize too large, max file size is {max_size_mb} MB", 400)