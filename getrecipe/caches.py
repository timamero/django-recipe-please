from django.core.cache import cache

class UserProfileCache:
    @staticmethod
    def set_user_profile(user_id, profile_data, timeout=3600):
        cache.set(f'user_profile_{user_id}', profile_data, timeout)

    @staticmethod
    def get_user_profile(user_id):
        return cache.get(f'user_profile_{user_id}')

    @staticmethod
    def delete_user_profile(user_id):
        cache.delete(f'user_profile_{user_id}')