from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Permission
from django.contrib.auth.decorators import login_required, permission_required
from .models import Transaction


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
            return redirect('home')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html', {})



@login_required
def home_view(request):
    if request.user.has_perm('myapp.view_all_transactions'):
        transactions = Transaction.objects.all()
    else:
        transactions = Transaction.objects.filter(payer=request.user)
    
    return render(request, 'home.html', {'transactions': transactions})



@permission_required('myapp.view_all_transactions', raise_exception=True)
def admin_view(request):
    transactions = Transaction.objects.all()
    return render(request, 'admin.html', {'transactions': transactions})

