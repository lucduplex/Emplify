from django.contrib import admin
from .models import User, Recruteur, Candidat, JobOffer

# Enregistrement du modèle User
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'role', 'statut', 'plan_abonnement')
    list_filter = ('role', 'statut', 'plan_abonnement')

# Enregistrement du modèle Recruteur
@admin.register(Recruteur)
class RecruteurAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'entreprise', 'secteur_activite', 'adresse')
    search_fields = ('entreprise', 'secteur_activite')

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

# Enregistrement du modèle Candidat
@admin.register(Candidat)
class CandidatAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'get_email', 'competences')
    search_fields = ('user__username',)

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'

    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'

# Enregistrement du modèle JobOffer
@admin.register(JobOffer)
class JobOfferAdmin(admin.ModelAdmin):
    list_display = ('titre', 'recruteur', 'localisation', 'date_publication')
    list_filter = ('localisation',)
    search_fields = ('titre', 'description')
