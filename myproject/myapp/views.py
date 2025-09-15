from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import MenuItem, GalleryImage, Testimonial
from .forms import TestimonialForm
from django.contrib.auth.decorators import login_required


def index(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    gallery_images = GalleryImage.objects.all()
    testimonials = Testimonial.objects.all()

    blends = menu_items.filter(category='blends')
    pastries = menu_items.filter(category='pastries')
    treats = menu_items.filter(category='treats')

    # Add the forms to the context
    testimonial_form = TestimonialForm()
    login_form = AuthenticationForm()

    context = {
        'blends': blends,
        'pastries': pastries,
        'treats': treats,
        'gallery_images': gallery_images,
        'testimonials': testimonials,
        'testimonial_form': testimonial_form,  # Pass the testimonial form
        'login_form': login_form,              # Pass the login form
    }
    return render(request, 'index.html', context)
def register(request):
    if request.method == 'POST':
        # Safely retrieve data using .get() to avoid KeyError
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('index')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('index')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already taken.')
            return redirect('index')
            
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('index')

        except Exception as e:
            # This handles any other unexpected errors, like password validation failures
            messages.error(request, f"An unexpected error occurred: {e}")
            return redirect('index')
            
    else:
        # On a GET request, render the index page where the form is located
        return render(request, 'index.html')
    

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
                # This now renders the index page, where your form is located
                return render(request, 'index.html', {'form': form})
        else:
            messages.error(request, "Invalid username or password.")
            # This also renders the index page
            return render(request, 'index.html', {'form': form})
    else:
        form = AuthenticationForm()
        # This renders the index page when the user first visits /login/
        return render(request, 'index.html', {'form': form})

def user_logout(request):
    auth.logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')



# The following view has been corrected
@login_required
def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial!')
            return redirect('index') 
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TestimonialForm()

    # Pass the form and all other context variables needed for index.html
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    gallery_images = GalleryImage.objects.all()
    testimonials_display = Testimonial.objects.all()

    context = {
        'blends': menu_items.filter(category='blends'),
        'pastries': menu_items.filter(category='pastries'),
        'treats': menu_items.filter(category='treats'),
        'gallery_images': gallery_images,
        'testimonials': testimonials_display,
        'form': form,
    }
    return render(request, 'index.html', context)