import pytest
from ...models import Profile
from ..utils import profile_data

@pytest.mark.django_db
class TestProfileModel:
    def test_auto_create_profile(self, user_instance):
        profile = Profile.objects.get(user=user_instance)
        assert profile.user == user_instance
    
    def test_update_profile(self, user_instance):
        data = profile_data()
        Profile.objects.filter(user=user_instance).update(**data)
        profile = Profile.objects.get(user=user_instance)
        assert profile.user == user_instance
        assert profile.full_name == data["full_name"]
        assert profile.bio == data["bio"]
        assert profile.birth_date == data["birth_date"]
    
    def test_profile_str(self, user_instance):
        profile = Profile.objects.get(user=user_instance)
        assert str(profile) == user_instance.username