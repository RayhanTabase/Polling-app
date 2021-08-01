import random
import os
# import environ
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
# from twilio.rest import Client
from .models import User, ActivationCode
from .forms import UserForm, ChangePasswordForm, EditProfileForm

HOST = "http://127.0.0.1:8000"
# env = environ.Env()
# environ.Env.read_env()

########### Account Registration And Activation ############

# Sign in/login of activated users
def login_view(request):
    # If a user is already logged in redirect to homepage
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:index"))

    error_message = ""

    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"].lower()
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        # If authentication successful
        if user is not None:
            # Cache current user logged in
            login(request, user)
            return HttpResponseRedirect(reverse("polls:index"))

        # If authentication failed
        else:
            error_message = "Invalid"
            # Check and redirect if user needs to be activated
            try:
                user = User.objects.get(username = username)
                if user.is_active == False:
                    return HttpResponseRedirect(reverse("user:activate_user",kwargs={"username":username}))
            # User does not exist
            except User.DoesNotExist:
                error_message ="User not found"
    return render(request,"user/login.html",context={"error_message":error_message})

# Log user out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("user:login"))

# Register new user
def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:index"))
    user_form = UserForm()
    error_messages = []

    if request.method == "POST":
        user_form = UserForm(request.POST, request.FILES)
        if user_form.is_valid():
            username = user_form.cleaned_data["username"]
            email = user_form.cleaned_data["email"]
            first_name = user_form.cleaned_data["first_name"]
            last_name = user_form.cleaned_data["last_name"]
            other_names = user_form.cleaned_data["other_names"]
            country_code = user_form.cleaned_data["country_code"] 
            phone_number = user_form.cleaned_data["phone_number"]
            profile_picture = request.FILES.get('profile_picture',False)
            password = user_form.cleaned_data["password"]
            date_of_birth = user_form.cleaned_data["date_of_birth"]
            
            # Attempt to create new user
            try:
                user = User.objects.create_user(
                    username = username, 
                    email = email, 
                    password = password,
                    first_name = first_name,
                    last_name = last_name,
                    other_names = other_names,
                    country_code = country_code,
                    phone_number = phone_number,
                    date_of_birth = date_of_birth,
                    profile_picture = profile_picture
                )
                # All new accounts are inactive until activated by otp code
                user.is_active = False
                user.save()
                create_activation_code(user.username)
                return HttpResponseRedirect(reverse("user:activate_user",kwargs={"username":username}))
            except IntegrityError:
                error_messages.append("Username already taken")
            except Exception as e:
                error_messages.append(e)
        else:  
            # Display all error fields as error message
            for field in user_form:   
                for error in field.errors:   
                    error_messages.append(error.capitalize())
    context ={
        "form":user_form,
        "error_messages":error_messages
    }
    return render(request, "user/register.html",context)

# Create a four key activation code
def create_activation_code(username):
    print("create activation code")
    code = random.randint(1000,9999) #simple code
    user = User.objects.get(username = username)
    # Check if user already has an activation code created and replace code
    try:
        user_activation = ActivationCode.objects.get(user = user)
        user_activation.code = code
        user_activation.save()
    #If user does not have activation code create new code for user
    except ActivationCode.DoesNotExist:
        new_activation_code = ActivationCode()
        new_activation_code.code = code
        new_activation_code.user = user
        new_activation_code.save()

    # Send activation code to users mobile using twilio api services
    # account_sid = env('ACCOUNT_SID')
    # auth_token = env('AUTH_TOKEN')
    # client = Client(account_sid, auth_token)
    try:
        # message = client.messages.create(
        #                                     body =f"Hello {user.first_name}, Your activation code is {code}",
        #                                     from_ =env('NUMBER'),
        #                                     to=user.phone_number
        #                                 )
        # print(message.sid)
        print(f"{username} activation code",code)
    except Exception:
        # Delete user if send otp failed; most likely phone number invalid
        user.delete()
       
        
# User atempt to activate account with key received
def activate_user(request, username):
    username = username.lower()
    # If user already activated redirect to home page
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("polls:index"))

    error_message = ""

    # Check if user exists in table for activation
    try:
        user = User.objects.get(username = username)
        user_code = ActivationCode.objects.get(user = user)
    except Exception:
        raise Http404
    
    if request.method == "POST":
        #Resend activation code to user phone  
        if request.POST["form_type"] == 'resend_code':
            create_activation_code(username)
            error_message = "Check your phone for code"
        
        # Try to activate user
        else:
            # Get database code
            code = user_code.code
            # Get user code input
            confirm_code = request.POST["code"]
            # Compare input with code and activate if same
            if code == confirm_code:
                user.is_active = True
                user.save()
                # delete activation code
                user_code.delete()
                return HttpResponseRedirect(reverse("user:login"))
            else:
                error_message = "Incorrect Code"

    context={
        "error_message":error_message,
        "username":username
    }
    return render(request, "user/activate_user.html",context)

############ Account Editing ##################

# Signed in user changes password
@login_required(login_url = 'user:login')
def change_password(request):
    user = request.user
    error_message = ""
    
    if request.POST:
        user = authenticate(username=user.username, password = request.POST["current_password"])
        # Check if authentication successful
        if user is not None:
            form = ChangePasswordForm(request.POST)
            if form.is_valid(): 
                if form.cleaned_data['new_password'] == form.cleaned_data['confirm_password'] :
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()
                    return HttpResponseRedirect(reverse('user:logout')) 
            error_message = "New password invalid"
        else:
            error_message = "Current password is incorrect"

    context = {
        "form": ChangePasswordForm(),
        "error_message":error_message
    }
    return render(request,"user/change_password.html",context)

# Send link for password reset to user's email
def reset_password_email(request):
    error_message = ""

    if request.method == "POST":
        email = request.POST["email"].lower()
        try:
            user = User.objects.get(email = email)
            token = user.password
            reset_link = f'{HOST}/reset_password/{user.id}/'
            print("This is the link for password reset (email)", reset_link, "  token is ",token)
            subject = "The SP Password Reset"
            body = f"Hello {user.first_name} {user.last_name}. Your token is --->     {token}        <---.Go to {reset_link}  to reset your password with token"
            receiver = user.email
            send_mail(
                subject,
                body,
                "",
                [receiver]
            )
            return HttpResponseRedirect(reverse("user:login"))
        except User.DoesNotExist:
            error_message = "Incorrect Email"
        except Exception as e:
            print(e)
            error_message = "Could not send mail to this email"
            # return HttpResponseRedirect(reverse("user:login"))
    context ={
        "error_message":error_message
    }
    return render(request, "user/reset_password_email.html", context)

# Link to enable users who forgot password to reset password
def reset_password_page(request,user_id):
    error_message = ""
    try:
        user = User.objects.get(id = user_id)
    except User.DoesNotExist:
        raise Http404

    if request.POST:
        token = request.POST["token"]
        # Check if current password token matches with provided token
        if not user.password == token:
            error_message = "Invalid token"

        else:
            form = ChangePasswordForm(request.POST)
            if form.is_valid():    
                try:
                    user.set_password(form.cleaned_data['new_password'])
                    user.save()  
                    return HttpResponseRedirect(reverse('user:login')) 
                except Exception as e:
                    error_message = str(e)
            else:
                error_message = str(form.errors)

    context = {
        "form": ChangePasswordForm(),
        "user_id": user_id,
        "error_message":error_message
    }
    return render(request,"user/reset_password_token.html",context)


# Change profile info
@login_required(login_url = 'user:login')
def edit_profile(request):
    error_message = ''

    if request.POST:
    
        form = EditProfileForm(request.POST, request.FILES)

        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            try:
                if not user.username == form.cleaned_data["username"]:
                    user.username = form.cleaned_data["username"]  
                new_profile_picture = request.FILES.get('new_profile_picture',False)
                if new_profile_picture:
                    if user.profile_picture:
                        try:
                            os.remove(user.profile_picture.path)
                        except:
                            print("couldn't remove old image")
                    user.profile_picture = new_profile_picture
                user.first_name = form.cleaned_data["first_name"]
                user.last_name = form.cleaned_data["last_name"]
                user.other_names = form.cleaned_data["other_names"]
                user.email = form.cleaned_data["email"]
                user.save()
                return HttpResponseRedirect(reverse('user:user_profile')) 
            except Exception as e:
                error_message = str(e)
        else:
            error_message = str(form.errors)

    if request.method == "DELETE":
        user = User.objects.get(username = request.user.username)
        user.delete()
        return HttpResponseRedirect(reverse("polls:index"))

    context ={
        "form": EditProfileForm(initial={
                    'username':request.user.username,
                    'first_name':request.user.first_name,
                    'last_name':request.user.last_name,
                    'other_names':request.user.other_names,
                    'email':request.user.email
                }),
        "error_message":error_message
    }
    return render(request,"user/edit_profile.html",context)

# Profile page
@login_required(login_url = 'user:login')
def user_profile(request):
    context={
        "page":"profile",
        "profile_form":UserForm(instance=request.user)
    }
    return render(request, "user/user_profile.html", context)
