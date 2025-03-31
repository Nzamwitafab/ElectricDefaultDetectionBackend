# core/services/profile_service.py

from core.repositories.profile_repository import ProfileRepository
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    @staticmethod
    def get_profile(user_id):
        logger.info(f"Retrieving profile for user with ID: {user_id}")
        profile = ProfileRepository.get_profile_by_user_id(user_id)
        if profile:
            logger.info(f"Profile found for user with ID: {user_id}")
            return profile
        logger.warning(f"Profile for user with ID {user_id} not found.")
        return None

    @staticmethod
    def update_profile(user_id, data):
        logger.info(f"Updating profile for user with ID: {user_id}")
        profile = ProfileRepository.get_profile_by_user_id(user_id)  # Ensure profile exists before updating
        if profile:
            # Proceed with updating if profile exists
            for field, value in data.items():
                setattr(profile, field, value)
            profile.save()
            logger.info(f"Profile updated for user with ID: {user_id}")
            return profile
        # If profile does not exist, log and return error message
        logger.warning(f"Profile for user with ID {user_id} not found for update.")
        return {"error": f"Profile for user with ID {user_id} not found, or invalid data provided."}

    @staticmethod
    def delete_profile(user_id):
        logger.info(f"Attempting to delete profile for user with ID: {user_id}")
        success = ProfileRepository.delete_profile(user_id)
        if success:
            logger.info(f"Profile deleted for user with ID: {user_id}")
            return True
        logger.warning(f"Profile for user with ID {user_id} not found for deletion.")
        return {"error": f"Profile for user with ID {user_id} not found for deletion."}
