from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import MenuItem, GalleryImage, Testimonial, UserProfile
from .forms import TestimonialForm, CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm, UserUpdateForm


def index(request):
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    gallery_images = GalleryImage.objects.all()
    testimonials = Testimonial.objects.filter(is_approved=True)

    blends = menu_items.filter(category='blends', is_available=True)
    pastries = menu_items.filter(category='pastries', is_available=True)
    treats = menu_items.filter(category='treats', is_available=True)

    # Add the forms to the context
    testimonial_form = TestimonialForm()

    context = {
        'blends': blends,
        'pastries': pastries,
        'treats': treats,
        'gallery_images': gallery_images,
        'testimonials': testimonials,
        'testimonial_form': testimonial_form,
    }
    return render(request, 'index.html', context)


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                messages.success(request, f"Welcome back, {user.first_name or username}!")
                return redirect('index')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'registration/login.html', {'form': form})


def user_logout(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('index')


@login_required
def profile(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_profile': user_profile,
    }
    return render(request, 'profile.html', context)


@login_required
def submit_testimonial(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            testimonial = form.save(commit=False)
            testimonial.user = request.user
            testimonial.save()
            messages.success(request, 'Thank you for your testimonial! It will be reviewed before being published.')
            return redirect('index') 
        else:
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = TestimonialForm()

    # Pass the form and all other context variables needed for index.html
    menu_items = MenuItem.objects.all().order_by('category', 'name')
    gallery_images = GalleryImage.objects.all()
    testimonials_display = Testimonial.objects.filter(is_approved=True)

    context = {
        'blends': menu_items.filter(category='blends', is_available=True),
        'pastries': menu_items.filter(category='pastries', is_available=True),
        'treats': menu_items.filter(category='treats', is_available=True),
        'gallery_images': gallery_images,
        'testimonials': testimonials_display,
        'form': form,
    }
    return render(request, 'index.html', context)