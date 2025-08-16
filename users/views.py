from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

def users_list(request):
    """Display list of all users."""
    users = User.objects.all()
    return render(request, 'users/users_list.html', {'users': users})

def user_detail(request, pk):
    """Display details of a specific user."""
    user = get_object_or_404(User, pk=pk)
    return render(request, 'users/user_detail.html', {'user_detail': user})

def user_create(request):
    """Create a new user."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/user_form.html', {'form': form})

def user_update(request, pk):
    """Update an existing user."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users_list')
    else:
        form = CustomUserChangeForm(instance=user)
    return render(request, 'users/user_form.html', {'form': form})

def user_delete(request, pk):
    """Delete a user."""
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        return redirect('users_list')
    return render(request, 'users/user_confirm_delete.html', {'user': user})
