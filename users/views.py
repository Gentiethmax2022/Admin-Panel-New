from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MyUser
from .forms import RegistrationForm
from django.utils import timezone
from django.http import HttpResponse


def login_view(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        remember_me = request.POST.get('remember_me', False)
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember_me:
                request.session.set_expiry(0)
            return redirect('users:dashboard')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html', {})



def register_view(request, *args, **kwargs):
    # user = request.user
    # if user.is_authenticated:
    #     return HttpResponse(f"You are already authenticated as {user.email}.")
    context = {}
    
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            destination = kwargs.get("next")
            if destination:
                return redirect(destination)
            return redirect('users:dashboard')
        
        else:
            print(form.errors)
            context['registration_form'] = form
            print(context)
            
    return render(request, 'registration.html', context)
        


@login_required
def dashboard_view(request):
    if request.user.has_perm('myapp.view_all_transactions'):
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.filter(payer=request.user)
    
    return render(request, 'dashboard.html', {'transactions': transactions})



@permission_required('myapp.view_all_transactions', raise_exception=True)
def admin_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'admin.html', {'transactions': transactions})

