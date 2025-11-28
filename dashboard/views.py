from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings
import random
from .models import TeamAdmin
from .utils import generate_password
from django.db import IntegrityError

def add_team_admin(request):
    if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        permission = request.POST.get('permissions')
        description = request.POST.get('description')

        # Validate empty fields
        if not first_name or not last_name or not email:
            messages.error(request, "All fields are required.")
            return redirect("teams")

        # Check if email exists
        if TeamAdmin.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect("teams")

        raw_password = generate_password()

        try:
            # Create admin
            TeamAdmin.objects.create(
                name=f"{first_name} {last_name}",
                username=f"STF-{random.randint(1000, 9999)}",
                email=email,
                permission=permission,
                description=description,
                password=make_password(raw_password)
            )
            print(raw_password)#EOHHN7ggw3
        except Exception as e:
            messages.error(request, f"Error creating admin: {e}")
            return redirect("teams")

        # Try sending email
        try:
            send_mail(
                subject="Your Admin Dashboard Login",
                message=f"Hello {first_name},\n\nYour admin password is: {raw_password}\nPlease keep it safe.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )
        except Exception as e:
            messages.warning(request, "Admin created, but email could not be sent.")
            return redirect("teams")

        messages.success(request, "Team admin created successfully!")
        return redirect("teams")

    return redirect("teams")


def admin_login(request):
    if request.method == "POST":
        email = request.POST.get("username")
        password = request.POST.get("password")

        try:
            admin = TeamAdmin.objects.get(email=email)
        except TeamAdmin.DoesNotExist:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")
        
        if not admin.verified:
            messages.error(request, "Your account is not verified. Please contact the administrator.")
            return render(request, "login.html")

        # Use Django's password checker
        if not check_password(password, admin.password):
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")

        # Set status to active
        admin.status = "active"
        admin.save()

        # Save session
        request.session["admin_id"] = admin.id
        request.session["admin_email"] = admin.email

        return redirect("dashboard_home")

    return render(request, "login.html")
def team_list(request):
    team_members = TeamAdmin.objects.all()  # fetch all members
    return render(request, 'dashboard/team.html', {'team_members': team_members})


def dashboard_login(request):
    return render(request, "login.html")


def dashboard_home(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    admin = TeamAdmin.objects.get(id=request.session["admin_id"])
    return render(request, 'dashboard/home.html', {"admin": admin})

def pending_jobs(request):
    return render(request, "dashboard/pending_jobs.html")


def pending_properties(request):
    return render(request, "dashboard/pending_properties.html")


def dashboard_messages(request):     # renamed
    return render(request, "dashboard/messages.html")


def users(request):
    return render(request, "dashboard/users.html")


def teams(request):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    admin = TeamAdmin.objects.get(id=request.session["admin_id"])
    team_members = TeamAdmin.objects.all()  # fetch all members
    return render(request, "dashboard/teams.html", {'team_members': team_members,"admin": admin})



def advertisement(request):
    return render(request, "dashboard/advertisement.html")


def reports(request):
    return render(request, "dashboard/reports.html")


def dashboard_settings(request): 
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    admin = TeamAdmin.objects.get(id=request.session["admin_id"])# renamed
    return render(request, "dashboard/settings.html",{"admin": admin})
def update_user_settings(request):
    if request.method == "POST":
        if "admin_id" not in request.session:
            return redirect("admin_login")
        
        admin = TeamAdmin.objects.get(id=request.session["admin_id"])
        
        # Get updated data from the form
        admin.name = request.POST.get("full_name", admin.name)
        admin.email = request.POST.get("email", admin.email)
        admin.phone_number = request.POST.get("phone_number", admin.phone_number)
        admin.permission = request.POST.get("role", admin.permission)
        admin.description = request.POST.get("description", admin.description)
        
        # Save the updated admin details
        admin.save()
        
        messages.success(request, "Settings updated successfully!")
        return redirect("settings")
    
    return redirect("settings")

def update_password(request):
    if request.method == "POST":
        if "admin_id" not in request.session:
            return redirect("admin_login")
        
        admin = TeamAdmin.objects.get(id=request.session["admin_id"])
        
        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_new_password = request.POST.get("confirm_new_password")
        
        # Check if current password is correct
        if not check_password(current_password, admin.password):
            messages.error(request, "Current password is incorrect.")
            return redirect("settings")
        
        # Check if new passwords match
        if new_password != confirm_new_password:
            messages.error(request, "New passwords do not match.")
            return redirect("settings")
        
        # Update password
        admin.password = make_password(new_password)
        admin.save()
        
        messages.success(request, "Password updated successfully!")
        return redirect("settings")
    
    return redirect("settings")

def delete_admin(request, admin_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    try:
        admin_to_delete = TeamAdmin.objects.get(id=admin_id)
        admin_to_delete.delete()
        
        request.session.flush()
        return redirect("a")
    except TeamAdmin.DoesNotExist:
        messages.error(request, "Team admin not found.")
   
    return redirect("settings")
def delete_team_admin(request, admin_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    try:
        admin_to_delete = TeamAdmin.objects.get(id=admin_id)
        admin_to_delete.delete()
        
        messages.success(request, "Team admin deleted successfully!")
    except TeamAdmin.DoesNotExist:
        messages.error(request, "Team admin not found.")
    
    return redirect("teams")

def verify_user(request, admin_id):
    if "admin_id" not in request.session:
        return redirect("admin_login")
    
    try:
        admin_to_verify = TeamAdmin.objects.get(id=admin_id)
        admin_to_verify.verified = True
        admin_to_verify.save()
        
        messages.success(request, "User verified successfully!")
    except TeamAdmin.DoesNotExist:
        messages.error(request, "User not found.")
    
    return redirect("teams")
def admin_logout(request):
    if "admin_id" in request.session:
        admin = TeamAdmin.objects.get(id=request.session["admin_id"])
        admin.status = "offline"
        admin.save()

    request.session.flush()
    return redirect("dashboard_login")

def update_profile_picture(request):
    if request.method == "POST":
        print("FILES:", request.FILES)

        admin = TeamAdmin.objects.get(id=request.session["admin_id"])

        if "profile_image" in request.FILES:
            f = request.FILES["profile_image"]
            print("UPLOAD FILE NAME:", f.name)

            admin.profile_image = f
            admin.save()

            print("STORED URL:", admin.profile_image.url)

        return redirect("settings")

