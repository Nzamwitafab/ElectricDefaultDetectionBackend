# core/services/user_service.py
import logging
from core.repositories.profile_repository import ProfileRepository
from core.repositories.user_repository import UserRepository
from rest_framework.exceptions import ValidationError # type: ignore
from rest_framework_simplejwt.tokens import RefreshToken # type: ignore
from rest_framework_simplejwt.authentication import JWTAuthentication # type: ignore
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed # type: ignore
from core.models import User
logger = logging.getLogger(__name__)  # Use Django's logging

def register_user(data):
    logger.info("Starting user registration process.")

    # Validate required fields
    if 'email' not in data or 'password' not in data:
        logger.warning("Validation failed: Missing required fields.")
        raise ValidationError("Email and Password are required fields.")

    # Check if user already exists
    if UserRepository.get_user_by_email(email=data['email']):
        logger.warning(f"User with email {data['email']} already exists.")
        raise ValidationError("A user with this email already exists.")

    # Validate password strength
    if len(data['password']) < 8:
        logger.warning("Password does not meet security requirements.")
        raise ValidationError("Password must be at least 8 characters long.")

    try:
        # Create the user
        user = UserRepository.create_user(data)
        logger.info(f"User {user.email} created successfully.")

        # Create a profile for the user
        profile_data = {"role": data.get("role")}
        ProfileRepository.create_profile(user, profile_data)
        logger.info(f"Profile created for user {user.email}.")

        return {"success": True, "message": "User registered successfully"}
    
    except Exception as e:
        logger.error(f"User registration failed: {str(e)}", exc_info=True)
        raise ValidationError("User registration failed due to an internal error.")


def login_user(data):
    email = data.get('email')
    password = data.get('password')

    print("\n=== DEBUG: Starting login process ===")
    print(f"1. Received credentials - Email: {email}, Password: [hidden]")

    if not email or not password:
        print("!! ERROR: Missing email or password")
        raise ValidationError("Email and Password are required fields.")

    print("2. Looking up user in database...")
    user = UserRepository.get_user_by_email(email)
    
    if user is None:
        # print(f"!! USER NOT FOUND: No user with email {email} exists")
        return None
    
    # print(f"3. User found - ID: {user.id}, Email: {user.email}")
    print("4. Verifying password...")
    
    if not user.check_password(password):
        print("!! PASSWORD MISMATCH: Provided password doesn't match stored hash")
        print(f"   Input password: {password}")
        print(f"   Stored password hash: {user.password}")
        return None
    
    print("5. Credentials verified successfully")
    print("6. Generating JWT tokens...")
    
    try:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        refresh_token = str(refresh)
        
        print("=== TOKEN GENERATION SUCCESS ===")
        print(f"Access token: {access_token}")
        print(f"Refresh token: {refresh_token}")
        print(f"Token payload: {refresh.access_token.payload}")  # Show token contents
        
        return {
            'access': access_token,
            'refresh': refresh_token
        }
    except Exception as e:
        print("!! TOKEN GENERATION FAILED")
        print(f"Error: {str(e)}")
        print(f"User details that failed token generation: ID={user.id}, Email={user.email}")
        return None
    
class CustomJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            user_id = validated_token['user_id']
            # Remove is_active check or add it to your User model
            return User.objects.get(id=user_id)  # Changed this line
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found', code='user_not_found')
        except KeyError:
            raise InvalidToken('Token contains no recognizable user identification')
        
def get_user_by_id(user_id):
    return UserRepository.get_user_by_id(user_id)

def get_all_users():
    return UserRepository.get_all_users()

def update_user(user_id, data):
    user = UserRepository.get_user_by_id(user_id)
    if not user:
        raise ValidationError("User not found.")

    # Email check
    if 'email' in data:
        existing_user = UserRepository.get_user_by_email(email=data['email'])
        if existing_user and existing_user.id != user_id:  # Ensure it's not the same user
            raise ValidationError("A user with this email already exists.")  

    # Password validation and hashing
    if 'password' in data:
        if len(data['password']) < 8:
            raise ValidationError("Password must be at least 8 characters long.")  
        user.set_password(data['password'])  # Properly hash the password
        data['password'] = user.password  # Store the hashed password

    # Proceed with the update
    return UserRepository.update_user(user_id, data)

def delete_user(user_id):
    return UserRepository.delete_user(user_id)
