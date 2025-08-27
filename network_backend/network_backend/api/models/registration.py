#it is creating the new table
# from django.db import models

# class UserRegistration(models.Model):
#     fullname = models.CharField(max_length=255)
#     email = models.EmailField(primary_key=True, max_length=255)  
#     password = models.CharField(max_length=255)

#     def __str__(self):
#         return self.email


#connect with table
from django.db import models

class UserRegistration(models.Model):
    fullname = models.CharField(max_length=255)
    email = models.EmailField(primary_key=True, max_length=255)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'user_registration'