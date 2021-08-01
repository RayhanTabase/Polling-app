import os
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser

def profile_image_upload_dir(instance, filename):
    return os.path.join(settings.BASE_DIR, f'media/profile_pictures/{instance.username}', filename)

class CustomError(Exception):
    pass

class User(AbstractUser):
    first_name = models.CharField(max_length=50, null=True) 
    last_name = models.CharField(max_length=50, null=True) 
    other_names = models.CharField(max_length=50, null=True, blank=True, default=" ")
    email = models.EmailField(unique=True)
    country_code = models.CharField(max_length=30,default="233",blank=True) 
    phone_number = models.CharField(max_length=30, unique=True)
    profile_picture = models.ImageField(null=True,blank=True,upload_to=profile_image_upload_dir, max_length =500)
    date_of_birth = models.DateField(null=True,blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

    def save(self, *args, **kwargs):
        # save all username and email in lowercase 
        self.username = self.username.lower()
        self.email = self.email.lower()

        # Password must be atleast 6 characters
        if len(self.password) < 6:
            raise CustomError("Min length is 6 characters for password")    
        #Username must be atleast 5 characters, first and last name must be atleast 2 characters
        if len(self.username) < 5:
            raise CustomError("Min length is 5 characters for username") 
        if self.first_name and len(self.first_name) < 2 or self.last_name and len(self.last_name) < 2 :
            raise CustomError("Min length is 2 characters for first name or last name") 
        #First name must be one word 
        if self.first_name and len(self.first_name.split()) > 1:
            raise CustomError("First name can must have only one name")
        #Last name must be one word 
        if self.last_name and len(self.last_name.split()) > 1:
            raise CustomError("Last name can must have only one name")
        # Phone number must be at least 9 digits
        if self.phone_number and len(self.phone_number) < 9:
            raise CustomError("Phone number length too short")
        super().save(*args, **kwargs)
        
    def delete(self):
        # Delete image file
        if self.profile_picture:
            try:
                os.remove(self.profile_picture.path)
            except Exception as e:
                print(e)
        super().delete()

    def serialize(self):
        image = None
        if self.profile_picture:
            image = self.profile_picture.url
        return {
            "name": f"{self.first_name} {self.other_names} {self.last_name}" ,
            "contact": self.country_code +"-"+ self.phone_number,
            "country_code": self.country_code,
            "phone": self.phone_number,
            "profile_picture": image
        }
        
class ActivationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #Users exists once in table
    code = models.CharField(max_length=4)