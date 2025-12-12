class UserFacingError(Exception):
    """Exception that should be displayed directly to users"""
    def __init__(self, message, status_code=200):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)