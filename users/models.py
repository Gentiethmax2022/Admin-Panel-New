from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser)
from django.utils import timezone


DISCOUNT_CODE_TYPE_CHOICES = [
    ('percent', 'Percentage-based'),
    ('value', 'Value-based'),
]

class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        
        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        
        return user 
    
    
    def create_superuser(self, email, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        
        return user 
    

class MyUser(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    date_of_birth = models.DateField()
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    balance = models.PositiveIntegerField(default=0)
    purchase_bonus = models.TextField(blank=True, default='')
    bonus_expiry_date = models.DateTimeField(null=True, blank=True)
    
    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth']
    
    def __str__(self):
        return self.email
    
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True 
    
    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True 
    
    @property
    def is_staff(self):
        """ Is the user  a member of staff 
        Simplest possible answer is that all admin are staff """
        return self.is_admin
    
    @property
    def has_negative_balance(self):
        "Does the user have a negative balance"
        return self.balance < 0
    
    @property  #type: ignore
    def has_sufficient_balance(self, payout):
        return self.balance >= payout
    
    @property
    def is_purchase_bonus_valid(self):
        if self.bonus_expiry_date is not None:
            return bool(self.purchase_bonus) and self.bonus_expiry_date > timezone.now()
        
    @property
    def transactions(self):
        received_transactions = self.received_transactions.all()  #type: ignore
        sent_transactions = self.sent_transactions.all()          #type:ignore
        transactions = list(received_transactions) + list(sent_transactions)
        transactions = sorted(transactions, key=lambda t: t.date, reverse=True)
        
        result = []
        for transaction in transactions:
            amount = transaction.amount
            if transaction.payee == self:
                amount = amount
            else:
                amount = -amount
            result.append(
                {
                    'date': transaction.date,
                    'description': transaction.description,
                    'amount': amount,
                    'category': transaction.category,
                    'payment_method': transaction.payment_method,
                    'reference_number': transaction.reference_number,
                    'status': transaction.status,
                    'attachments': transaction.attachments,
                }
            )
        
        return result



class Transaction(models.Model):
    CATEGORY_CHOICES = (
        ('income', 'Income'),
        ('expenses', 'Expenses'),
        ('investments', 'Investments'),
        ('transfers', 'Transfers'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    payer = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='sent_transactions')
    payee = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    payment_method = models.CharField(max_length=50)
    reference_number = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)
    
    
    class Meta:
        ordering = ['-date']
        permissions = [
            ("view_own_transactions", "Can view own transactions"),
            ("view_all_transactions", "Can view all transactions"),
        ]
        
    def __str__(self) -> str:
        return self.description
    
    
    
    
