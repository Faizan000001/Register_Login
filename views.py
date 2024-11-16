from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from .models import User
import datetime

def index(request):
    if request.method == 'GET':
        # Context for prepopulating dropdowns in the form
        context = {
            'days': range(1, 32),
            'months': ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
            'years': range(1980, 2025),
        }
        return render(request, 'index.html', context)

    elif request.method == 'POST':
        data = request.POST
        action = data.get('action')

        if action == 'register':
            # Check if the email already exists
            if User.objects.filter(email=data.get('email')).exists():
                return JsonResponse({"status": "error", "message": "Email already exists."})

            # Validate and parse date of birth
            year = data.get('year')
            month = data.get('month')
            date = data.get('date')

            try:
                months_map = {
                    "January": "01", "February": "02", "March": "03", "April": "04",
                    "May": "05", "June": "06", "July": "07", "August": "08",
                    "September": "09", "October": "10", "November": "11", "December": "12"
                }
                month_number = months_map.get(month)
                dob = datetime.datetime.strptime(f"{year}-{month_number}-{date.zfill(2)}", "%Y-%m-%d").date()
            except ValueError:
                return JsonResponse({"status": "error", "message": "Invalid date of birth."})

            # Save user to the database
            user = User(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                email=data.get('email'),
                password=make_password(data.get('password')),  # Hash the password
                dob=dob,
                gender=data.get('gender')
            )
            user.save()
            return JsonResponse({"status": "success", "message": "User registered successfully!", "reset_form": True})

        elif action == 'login':
            data = request.POST
            try:
                # Check if the user exists and validate password
                user = User.objects.get(email=data.get('email'))
                if check_password(data.get('password'), user.password):
                    return JsonResponse({"status": "success", "message": "Login successful!", "reset_form": True})
                else:
                    return JsonResponse({"status": "error", "message": "Invalid password."})
            except User.DoesNotExist:
                return JsonResponse({"status": "error", "message": "Invalid email."})

        return JsonResponse({"status": "error", "message": "Invalid action!"})

    return JsonResponse({"status": "error", "message": "Invalid HTTP method."})
