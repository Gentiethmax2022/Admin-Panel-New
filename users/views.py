from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import MyUser
from .forms import RegistrationForm, TransactionForm, UserProfileForm
from django.utils import timezone
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.db.models import Q
from datetime import datetime, timedelta 



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
    try:
        user_group = Group.objects.get(name='user_group')
    except Group.DoesNotExist:
        user_group = None

    # Calculate the datetime 24 hours ago
    time_24_hours_ago = datetime.now() - timedelta(hours=24)

    # Get the user's group names
    user_group_names = [g.name for g in user.groups.all()]

    context = {
        'transactions': transactions,
        'admin_group': admin_group,
        'time_24_hours_ago': time_24_hours_ago,
        'user_group': user_group,
        'user_group_names': user_group_names,  # Add the user's group names to the context
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


@login_required
def modify_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == "POST":
        # update the transaction fields
        transaction.description = request.POST['description']
        transaction.status = request.POST['status']
        if 'attachments' in request.FILES:
            transaction.attachments = request.FILES['attachments']
        transaction.save()
        return redirect('users:dashboard')  # or another URL where you want to redirect the user after modification
    
    return render(request, 'modify_transaction.html', {'transaction': transaction})


@login_required
def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    
    if request.method == "POST":
        transaction.delete()
        return redirect('users:dashboard')  # or another URL where you want to redirect the user after deletion
    
    return render(request, 'delete_transaction.html', {'transaction': transaction})




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
    

@login_required
def update_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:user_profile')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'update_profile.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('users:login')

