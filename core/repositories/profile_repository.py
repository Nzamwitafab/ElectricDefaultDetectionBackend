from core.models import Profile

class ProfileRepository:
    @staticmethod
    def create_profile(user, profile_data=None):
        if profile_data is None:
            profile_data = {}

        profile, created = Profile.objects.get_or_create(user=user, defaults=profile_data)
        if not created:
            print(f"Profile for user {user.email} already exists.")
        return profile

    @staticmethod
    def get_profile_by_user_id(user_id):
        try:
            return Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return None

    @staticmethod
    def update_profile(user_id, data):
        profile = ProfileRepository.get_profile_by_user_id(user_id)
        if profile:
            for field, value in data.items():
                setattr(profile, field, value)
            profile.save()
            return profile
        return None

    @staticmethod
    def delete_profile(user_id):
        profile = ProfileRepository.get_profile_by_user_id(user_id)
        if profile:
            profile.delete()
            return True
        return False
