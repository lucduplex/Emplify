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
    path('upload_resume/', views.upload_resume, name='upload_resume'), 
    path('search_job_offers/', views.search_job_offers, name='search_job_offers'),  
    path('job_detail/<int:offre_id>/', views.job_detail, name='job_detail'), 
    path('postuler_offre/<int:offre_id>/', views.postuler_offre, name='postuler_offre'),
    path('mes_candidatures/', views.mes_candidatures, name='mes_candidatures'),
    path('', views.index, name='index'),
    path('match_jobs/', views.match_jobs_view, name='match_jobs'),
    path('offre/<int:offre_id>/generate_cover_letter/', views.generate_cover_letter, name='generate_cover_letter'),
    path('offre/<int:offre_id>/download_cover_letter_pdf/', views.download_cover_letter_pdf, name='download_cover_letter_pdf'),
      path('chatbot/', views.chatbot_page, name='chatbot_page'),
    path('chatbot/response/', views.chatbot_response, name='chatbot_response'),


]
