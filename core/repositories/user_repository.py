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


    @staticmethod
    def get_user_by_id(user_id):
        return User.objects.filter(id=user_id).first()

    @staticmethod
    def get_all_users():
        return User.objects.all()

    @staticmethod
    def update_user(user_id, data):
        user = User.objects.filter(id=user_id).first()
        if user:
            for key, value in data.items():
                setattr(user, key, value)
            user.save()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.objects.filter(id=user_id).first()
        if user:
            user.delete()
        return user
