from flask import session
import bcrypt, re
from .config import get_config
from .repository.users import UsersService
from .repository.database import DatabaseService
from ..exceptions import UserFacingError

class AuthService:

    # Unique session variable name for storing user_data
    user_data_session_name = 'meeting_notes_bot_user_data'

    # More round make password hashing take longer but help mitigate bruce force attacks
    password_hash_salt_rounds = 12

    # Basic regex to validate emails
    valid_email_regex = r"[^@\s]+@[^@\s]+\.[^@\s]+"

    def __init__(self, db: DatabaseService):
        self.users_service = UsersService(db)

    def signup(self, name, email, password):

        self._validate_email(email)
        self._validate_password(password)

        default_prompt = get_config("default_user_prompt")
        password_hash = self._get_hashed_password(password)

        self.users_service.create(name, email, password_hash, default_prompt)

        client_side_user_data = self.login(email, password)
        
        return client_side_user_data

    def login(self, email, password):
        user_data = self.users_service.get(user_email=email)

        if not user_data:
            raise UserFacingError("Invalid email or password")

        success = self._check_password(password, user_data['password_hash'])

        if not success:
            raise UserFacingError("Invalid email or password")

        self.user_data = user_data
        client_side_user_data = self.get_client_side_user_data(user_data)
        return client_side_user_data

    def logout(self):
        del self.user_data
        return True
    
    def is_logged_in(self):
        return bool(self.user_data)
    
    def get_user_id(self):
        if not self.user_data:
            return None
        return self.user_data['id']
    
    def get_client_side_user_data(self, user_data = None):

        if not user_data:
            user_data = self.user_data

        client_side_user_data_keys = ['name', 'email', 'default_prompt', 'created_at']
        
        client_side_user_data = dict((k, user_data[k]) for k in client_side_user_data_keys if k in user_data)
        return client_side_user_data
    
    def update_user(self, name: str, default_prompt: str):
        
        user_id = self.user_data['id']
        self.users_service.update(user_id, name, default_prompt)
        
        # Update session data
        updated_user_data = self.users_service.get(user_id=user_id)
        self.user_data = updated_user_data
        
        return self.get_client_side_user_data(updated_user_data)
    
    def _validate_email(self, email):
        if not re.match(self.valid_email_regex, email):
            raise UserFacingError("Invalid Email address")
    
    def _validate_password(self, password):
        if len(password) < 8:
            raise UserFacingError("Invalid Password, password must be at least 8 characters long")

    def _get_hashed_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(self.password_hash_salt_rounds))

    def _check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
    
    # The user_data property can be used to control the user_data in the session variable.
    @property
    def user_data(self):
        return session.get(self.user_data_session_name)
    @user_data.setter
    def user_data(self, user_data):
        session[self.user_data_session_name] = user_data
    @user_data.deleter
    def user_data(self):
        session.pop(self.user_data_session_name, None)