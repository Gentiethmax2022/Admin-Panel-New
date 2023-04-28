from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MyUser
from .forms import RegistrationForm, TransactionForm, UpdateProfileImageForm
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.db.models import Q



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
    user = request.user
    if user.has_perm('users.view_all_transactions'):
        transactions = Transaction.objects.all()
    elif user.has_perm('users.view_own_transactions'):
        transactions = Transaction.objects.filter(Q(payer=user) | Q(payee=user))
    else:
        transactions = []  # If the user has neither permission, show an empty list

    admin_group = Group.objects.get(name='admin_group')

    context = {
        'transactions': transactions,
        'admin_group': admin_group,
    }
    return render(request, 'dashboard.html', context)




def risk_assessment(request):
    transactions = Transaction.objects.all()
    return render(request, 'risk_assessment.html', {'transactions': transactions})


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

def user_is_authenticated(user):
    return user.is_authenticated



@user_passes_test(user_is_authenticated)
def user_profile_view(request):
    all_users = MyUser.objects.all()
    current_user = request.user
    context = {
        'all_users': all_users,
        'current_user': current_user,
    }
    return render(request, 'user_profile.html', context)



def search_transactions(request):
    query = request.GET.get('q')
    transactions = Transaction.objects.filter(payer__email__icontains=query) | Transaction.objects.filter(payee__email__icontains=query)
    context = {'transactions': transactions, 'query': query}
    return render(request, 'search_transactions.html', context)


def reports(request):
    return render(request, 'reports.html', {})


@login_required
def new_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST, request.FILES)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.payer = request.user
            transaction.save()
            messages.success(request, 'Transaction created successfully.')
            return redirect('users:dashboard') # Replace 'dashboard' with the name of the view where you want to redirect after a successful transaction creation
    else:
        form = TransactionForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'new_transaction.html', context)


def home_view(request):
    return render(request, 'home.html', {})
    

def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES)
        if form.is_valid():
            request.user.profile_image = form.cleaned_data['profile_image']
            request.user.save()
            return redirect('users:user_profile')  # Replace 'profile' with the name of your profile view
    else:
        form = UpdateProfileImageForm()
    return render(request, 'user_profile.html', {'form': form})


def update_profile_image(request):
    if request.method == 'POST':
        form = UpdateProfileImageForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')
    else:
        form = UpdateProfileImageForm(instance=request.user)

    context = {'form': form}
    return render(request, 'update_profile_image.html', context)

