from faker import Faker

faker = Faker()

def user_valid_data() -> dict:
    return {
        "email":faker.email(),
        "username":faker.user_name(),
        "password":"Aa123456@"
    }

def user_invalid_data() -> dict:
    return {
        "email": "not-an-email",
        "username": "a!",
        "password": "123"
    }

def profile_data() -> dict:
    return {
        "full_name":faker.first_name() + faker.last_name(),
        "bio":faker.paragraph(),
        "birth_date":faker.date_of_birth(),
    }