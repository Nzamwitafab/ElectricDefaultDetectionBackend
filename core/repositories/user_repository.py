# core/repositories/user_repository.py
from core.models import User

class UserRepository:
    @staticmethod
    def create_user(data):
        # Create a new user via the UserManager in the model
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            name=data['name'],
            phone_number=data['phone_number'],
            role=data['role']
        )
        return user

    @staticmethod
    def get_user_by_email(email):
        return User.objects.filter(email=email).first()

    