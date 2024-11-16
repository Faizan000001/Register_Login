from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # Make sure to hash passwords!
    dob = models.DateField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.email
