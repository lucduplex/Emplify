# app/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, JobOffer , Candidat, Candidature
from django.core.exceptions import ValidationError


class RegistrationForm(UserCreationForm):
    """Formulaire d'inscription utilisateur"""
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'role', 'plan_abonnement']

class LoginForm(forms.Form):
    """Formulaire de connexion"""
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class JobForm(forms.ModelForm):
    """Formulaire de publication d'offre d'emploi"""
    class Meta:
        model = JobOffer
        fields = ['titre', 'description', 'competences_requises', 'salaire', 'localisation']
class CandidatForm(forms.ModelForm):
    """Formulaire de candidature, ajoutez une validation pour les formats de fichiers """
    class Meta:
        model = Candidat
        fields = ['cv', 'competences', 'lettres_motivation']

    def clean_cv(self):
        cv = self.cleaned_data.get('cv')
        if cv:
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not any(cv.name.endswith(ext) for ext in valid_extensions):
                raise ValidationError('Le CV doit être au format PDF ou Word.')
        return cv

    def clean_lettres_motivation(self):
        lettre = self.cleaned_data.get('lettres_motivation')
        if lettre:
            valid_extensions = ['.pdf', '.doc', '.docx']
            if not any(lettre.name.endswith(ext) for ext in valid_extensions):
                raise ValidationError('La lettre de motivation doit être au format PDF ou Word.')
        return lettre
    
class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = []    