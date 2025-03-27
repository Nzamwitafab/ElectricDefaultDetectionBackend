# core/services/user_service.py
from core.repositories.user_repository import UserRepository
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
from core.models import User
def register_user(data):
    # Validate required fields
    if 'email' not in data or 'password' not in data:
        raise ValidationError("Email and Password are required fields.")
    
    # Check if user already exists
    if UserRepository.get_user_by_email(email=data['email']):
        raise ValidationError("A user with this email already exists.")
    
    # Validate password strength (optional)
    if len(data['password']) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    
    # Create the user
    user = UserRepository.create_user(data)
    return user


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