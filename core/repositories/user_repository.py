# core/repositories/user_repository.py
from core.models import User

class UserRepository:
    @staticmethod
    def create_user(data):
        user = User.objects.create_user(
            email=data['email'],
            password=data['password'],
            name=data.get('name'),
            phone_number=data.get('phone_number'),
            role=data.get('role')
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
