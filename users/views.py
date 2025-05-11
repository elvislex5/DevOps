from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login, logout
from .models import User
from django import forms
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponse

class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    
    def get_success_url(self):
        messages.success(self.request, 'Connexion réussie! Bienvenue.')
        return reverse_lazy('dashboard')

class CustomLogoutView(LogoutView):
    next_page = 'home'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Vous avez été déconnecté avec succès.')
        return super().dispatch(request, *args, **kwargs)

class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'role', 'company', 'phone']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-select'}),
            'company': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Les mots de passe ne correspondent pas.')
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'total_projects': 0,  # À remplacer par la vraie logique
        'active_projects': 0,  # À remplacer par la vraie logique
        'upcoming_tasks': [],  # À remplacer par la vraie logique
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    return render(request, 'users/profile.html', {'user': request.user})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    return render(request, 'users/profile_edit.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Votre compte a été créé avec succès!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'company', 'profile_picture']
        labels = {
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
            'phone': 'Téléphone',
            'company': 'Entreprise',
            'profile_picture': 'Photo de profil',
        }

@login_required
def profile_fragment(request):
    html = render_to_string('users/profile.html', {'user': request.user})
    return HttpResponse(html)

@login_required
def profile_edit_fragment(request):
    form = UserProfileForm(instance=request.user)
    html = render_to_string('users/profile_edit.html', {'form': form})
    return HttpResponse(html)
