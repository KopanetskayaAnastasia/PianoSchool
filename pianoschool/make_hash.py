from django.contrib.auth.hashers import make_password

password = 'NewPassword123'
hash = make_password(password)
print("Hash for Django:", hash)