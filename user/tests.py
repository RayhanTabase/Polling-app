from django.test import TestCase, Client
from .models import User, ActivationCode
from .views import create_activation_code
from django.core.files.uploadedfile import SimpleUploadedFile

SMALL_GIF =  (
    b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x00\x00\x00\x21\xf9\x04'
    b'\x01\x0a\x00\x01\x00\x01\x00\x2c\x00\x00\x02\x00\x02\x00\x00\x02'
    b'\x02\x4c\x01\x00\x3b'
)
# TEST_PICTURE = SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif')

class BreakOutError(Exception):
    pass

# Test Models
class UserTest(TestCase):
    def setUp(self):
        self.client = Client()

        #Create users 
        self.user1 = User.objects.create_user(
            username ="user1",
            password ="userpassword",
            first_name = "Kofi",
            last_name = "Aban",
            other_names = "Wood" ,
            email ="KofiAb@wood.com",
            country_code ="233", 
            phone_number ="123456789",
            profile_picture="test_image.jpg",
        )
        self.user2 = User.objects.create_user(
            username ="user2",
            password ="userpassword",
            first_name = "Ama",
            last_name = "Attaido",
            other_names = "Jessy" ,
            email ="AmmaAtta@jessy.com",
            country_code ="233", 
            phone_number ="222256789",
            profile_picture="test_image.jpg",
        )
        self.user2.is_active = False
        create_activation_code(self.user2.username)

    def test_get__database(self):
        # Get user1
        try:
            User.objects.get(username ='user1')
        except Exception as e:
            raise Exception(e)
        self.assertEqual(len(User.objects.all()),2)

    def test_activate_user2(self):
        try:
            user2_activation = ActivationCode.objects.get(user = self.user2)
            user2_activation_code = user2_activation.code
        except Exception as e:
            raise Exception(e)
        try:
            user2 = User.objects.get(username ='user2')
            user2.is_active = True
            user2.save()
        except Exception as e:
            print(e)
            raise Exception("Failed to activate user 2")

    def test_username_integrity(self):
        try:
            User.objects.create(
                username ="USER1",
                password ="userpassword",
                first_name = "Kofi",
                last_name = "Aban",
                other_names = "Wood" ,
                email ="KofiAb1@wood.com",
                country_code ="233", 
                phone_number ="9099956789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, username integrity error should be triggered")
        except Exception as e:
            pass

    def test_email_integrity(self):
        try:
            User.objects.create(
                username ="user123",
                password ="userpassword",
                first_name = "Kofi",
                last_name = "Aban",
                other_names = "Wood" ,
                email ="KOFIAB@wood.com",
                country_code ="233", 
                phone_number ="2233456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, email integrity error should be triggered")
        except Exception as e:
            pass

    def test_phone_number_integrity(self):
        try:
            User.objects.create(
                username ="user123",
                password ="userpassword",
                first_name = "Kofi",
                last_name = "Aban",
                other_names = "Wood" ,
                email ="KofiAb12@wood.com",
                country_code ="233", 
                phone_number ="123456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, phone number integrity error should be triggered")
        except Exception as e:
            pass

    def test_user_minimum_password(self):
        try:
            User.objects.create(
                username ="test_user",
                password ="123",
                first_name = "Poon",
                last_name = "Boon",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, minimum password length error should have been triggered")
        except Exception as e:
            pass
    
    def test_username_min_length(self):
        try:
            User.objects.create(
                username ="user",
                password ="1234567",
                first_name = "Poon",
                last_name = "Boon",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, minimum username length error should be triggered")
        except Exception as e:
            pass

    def test_firstname_min_length(self):
        try:
            User.objects.create(
                username ="test_user",
                password ="1234567",
                first_name = "f",
                last_name = "Boon",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, minimum firstname length error should be triggered")
        except Exception as e:
            pass

    def test_lastname_min_length(self):
        try:
            User.objects.create(
                username ="test_user",
                password ="1234567",
                first_name = "first",
                last_name = "l",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, minimum lastname length error should be triggered")
        except Exception as e:
            pass

    def test_firstname_one_word(self):
        try:
            User.objects.create(
                username ="test_user",
                password ="1234567",
                first_name = "first another",
                last_name = "lastly",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, first name one word error")
        except Exception as e:
            pass

    def test_lastname_one_word(self):
        try:
            User.objects.create(
                username ="test_user",
                password ="1234567",
                first_name = "firstly",
                last_name = "last man standing",
                other_names = "Woon" ,
                email ="BoonB@woon.com",
                country_code ="233", 
                phone_number ="555456789",
                profile_picture="test_image.jpg",
            )
            raise BreakOutError()
        except BreakOutError:
            raise Exception("Creation of user should have failed, last name one word error")
        except Exception as e:
            pass

    ##### Test Pages

    # Test get requests
    def test_register_page(self):
        response = self.client.get("/register/")
        self.assertEqual(response.status_code, 200)
        try:
            self.assertTrue(response.context['form'])
        except Exception:
            raise Exception("Registration form missing")

    def test_login_page(self):
        response = self.client.get("/login/")
        self.assertEqual(response.status_code, 200)

    def test_logout_page(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 302)
    
    def test_activate_user_page(self):
        response = self.client.get("/activate/user2/")
        self.assertEqual(response.status_code, 200)

    def test_user_profile_page(self):

        #Test profile page redirect no logged in user
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 302)

        # Test profile page logged in user
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/user/profile/")
        self.assertEqual(response.status_code, 200)

    def test_send_reset_email_page(self):
        response = self.client.get("/send_reset_email/")
        self.assertEqual(response.status_code, 200)

    def test_edit_user_profile_page(self):
        # Unlogged in user
        response = self.client.get("/user/edit/")
        self.assertEqual(response.status_code, 302)
        #logged in user
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/user/edit/")
        self.assertEqual(response.status_code, 200)

    def test_change_password(self):
        response = self.client.get("/user/change_password/")
        self.assertEqual(response.status_code, 302)
        #logged in user
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.get("/user/change_password/")
        self.assertEqual(response.status_code, 200)

    def test_reset_password_token_page(self):
        # Correct credentials user1
        response = self.client.get("/reset_password/1/")
        self.assertEqual(response.status_code, 200)

        # Incorrect credentials
        response = self.client.get("/reset_password/300/")
        self.assertEqual(response.status_code, 404)
        
    # Test post requests
    
    def test_register_page_invalid_post(self):
        response = self.client.post("/register/", {
                'username': 'user1',
                'password': 'super22',
                'confirm_password': 'super227',
                "first_name" : "K",
                "last_name" : "John Mensah",
                "other_names" : "J E" ,
                "email" :"KofiAb@wood.com",
                "country_code" :"233", 
                "phone_number" :"123456789",
                "profile_picture" : SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
            }
        )
        self.assertEqual(response.status_code, 200)
        # Check errors: username exists,first name error,  last name error, phone error, password error
        self.assertEqual(len(response.context['error_messages']),5) 

    def test_login_page_post(self):
        '''Test login valid credentials '''

        # Wrong user credentials should return 200
        response = self.client.post("/login/", {'username': 'wrongusername', 'password': 'userpassword'})
        self.assertEqual(response.status_code, 200)

        # Inactive user2 should redirect 302
        response = self.client.post("/login/", {'username': 'user2', 'password': 'userpassword'})
        self.assertEqual(response.status_code, 302)
        
        response = self.client.post("/login/", {'username': 'user1', 'password': 'userpassword'})
        self.assertEqual(response.status_code, 302)

    def test_activate_user_post(self):
        # Test incorrect code
        response = self.client.post("/activate/user2/", {'code':0000,"form_type":"activate"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['error_message']) 

        # Test resend code
        response = self.client.post("/activate/user2/", {'code':0000,"form_type":"resend_code"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['error_message']) 

        user2_activation = ActivationCode.objects.get(user__username__icontains = "user2")
        user_code = user2_activation.code

        # Test correct code
        response = self.client.post("/activate/user2/", {'code':user_code,"form_type":"activate"})
        self.assertEqual(response.status_code, 302)

    def test_send_reset_email_page(self):
        # Test incorrect email
        response = self.client.post("/send_reset_email/",{
            "email":"incorrectone@incorrect.com"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['error_message']) 
 
        # Test correct email
        response = self.client.post("/send_reset_email/",{
            "email":"KofiAb@wood.com"
        })
        if response.status_code == 302:
            return
        if "Could not send mail" in response.context['error_message'] :
            return
        raise Exception("Email did not match any in the database")
        
    def test_edit_user_profile_page_2_post(self):
        '''Inalid user edit'''
        self.client.login(username ="user1",password ="userpassword")
        response = self.client.post("/user/edit/",{
            "username": "user2",
            "first_name" : "Kwame",
            "last_name" : "Babone" ,
            "other_names" :"Y K",
            "new_profile_picture": SimpleUploadedFile("small.gif", SMALL_GIF , content_type='image/gif'),
        })
        self.assertTrue(response.context['error_message']) 

    def test_change_password(self):
        self.client.login(username ="user1",password ="userpassword")
        # Check invalid current password
        response = self.client.post("/user/change_password/",{
            "current_password": "userpass",
            "new_password": "newpassword",
            "confirm_password" : "newpassword" 
        })
        self.assertTrue(response.context['error_message'])
       
        # Check invalid new password
        response = self.client.post("/user/change_password/",{
            "current_password": "userpassword",
            "new_password": "newpass",
            "confirm_password" : "newpassword" 

        })
        self.assertTrue(response.context['error_message'])

        # Check Valid edit
        response = self.client.post("/user/change_password/",{
            "current_password": "userpassword",
            "new_password": "newpassword",
            "confirm_password" : "newpassword" 

        })
        self.assertEqual(response.status_code, 302)

    def test_token_password_reset_post(self):
        # Check valid change
        user = User.objects.get(username__icontains = "user1")
        response = self.client.post("/reset_password/1/",{
            "token":user.password,
            "new_password": "newpassword",
            "confirm_password" : "newpassword" 
        })
        self.assertEqual(response.status_code, 302)
        #Check invalid password
        response = self.client.post("/reset_password/1/",{
            "token":user.password,
            "new_password": "new",
            "confirm_password" : "new" 
        })
        self.assertEqual(response.status_code, 200)
        #Check wrong token
        response = self.client.post("/reset_password/1/",{
            "token":"token",
            "new_password": "newpassword",
            "confirm_password" : "newpassword" 
        })
        self.assertEqual(response.status_code, 200)
        # Check unmatching password
        response = self.client.post("/reset_password/1/",{
            "token":user.password,
            "new_password": "newpassword",
            "confirm_password" : "newpasswo" 
        })
        self.assertEqual(response.status_code, 200)