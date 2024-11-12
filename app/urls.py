# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('offres/', views.job_list, name='job_list'),
    path('offres/poster/', views.post_job, name='post_job'),
    path('profil/', views.profile, name='profile'),
    path('inscription/', views.register, name='register'),
    path('connexion/', views.login_view, name='login'),
    path('deconnexion/', views.logout_view, name='logout'),
    path('about/', views.about_view, name='about'),
    path('upload_resume/', views.upload_resume, name='upload_resume'),  # URL pour le téléchargement de CV et lettre de motivation
    path('search_job_offers/', views.search_job_offers, name='search_job_offers'),  # URL pour la recherche d'offres d'emploi
    path('job_detail/<int:offre_id>/', views.job_detail, name='job_detail'),  # URL pour les détails de l'offre
    path('postuler_offre/<int:offre_id>/', views.postuler_offre, name='postuler_offre'),
    path('mes_candidatures/', views.mes_candidatures, name='mes_candidatures'),
]
