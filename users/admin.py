from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import MyUser, Transaction
from django.forms.fields import ImageField


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)
    profile_image = forms.ImageField(label='Profile Image', required=False)
    
    class Meta:
        model = MyUser
        fields = ('email', 'date_of_birth', 'balance', 'profile_image')
        
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    profile_image = forms.ImageField(label='Profile Image', required=False)
    
    class Meta:
        model = MyUser
        fields = ('email', 'password', 'date_of_birth', 'is_active', 'is_admin', 'balance', 'profile_image')
    
    def clean_password(self):
        return self.initial["password"]
    

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    
    list_display = ('email', 'date_of_birth', 'date_joined', 'last_login', 'is_admin', 'is_staff', 'balance', 'profile_image')
    list_filter = ('is_admin', 'is_staff')
    search_fields = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'profile_image')}),
        ('Permissions', {'fields': ('is_admin',)}),
        ('Site Info', {'fields': ('balance', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2', 'balance', 'profile_image'),
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()
    
    
admin.site.register(MyUser, UserAdmin)



class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'payer', 'payee', 'amount', 'category', 'status']
    list_filter = ('category', 'status')
    search_fields = ('payer__username', 'payee_username', 'description', 'reference_number')
    

admin.site.register(Transaction, TransactionAdmin)


