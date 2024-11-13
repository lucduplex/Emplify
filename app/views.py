# app/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import JobForm, RegistrationForm, LoginForm, CandidatForm, CandidatureForm
from .models import Recruteur, JobOffer, Candidature ,Candidat
from django.core.files.storage import default_storage
from django.contrib import messages
import os

def index(request):
    jobs = JobOffer.objects.all()[:6] 
    return render(request, 'index.html', {'jobs': jobs})

def job_list(request):
    """Liste des offres d'emploi disponibles"""
    jobs = JobOffer.objects.all()
    return render(request, 'job_list.html', {'jobs': jobs})

@login_required
def post_job(request):
    """Publier une offre d'emploi (réservé aux recruteurs)"""
    if request.user.role == 'RECRUTEUR':
        if not hasattr(request.user, 'recruteur_profile'):
            # Crée un profil recruteur s'il n'existe pas
            Recruteur.objects.create(user=request.user)

        if request.method == 'POST':
            form = JobForm(request.POST)
            if form.is_valid():
                job = form.save(commit=False)
                job.recruteur = request.user.recruteur_profile
                job.save()
                return redirect('job_list')
        else:
            form = JobForm()
        return render(request, 'post_job.html', {'form': form})
    else:
        return redirect('job_list')  # Les candidats ne peuvent pas accéder à cette vue


@login_required
def profile(request):
    """Profil utilisateur"""
    return render(request, 'profile.html', {'user': request.user})

def register(request):
    """Inscription de nouveaux utilisateurs"""
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Connecte l'utilisateur automatiquement après l'inscription
            return redirect('index')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    """Connexion utilisateur"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                form.add_error(None, 'Nom d’utilisateur ou mot de passe incorrect')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def logout_view(request):
    """Déconnexion utilisateur"""
    logout(request)
    return redirect('index')

@login_required
def upload_resume(request):
    """Télécharger CV et lettre de motivation pour les candidats"""
    if request.method == 'POST':
        form = CandidatForm(request.POST, request.FILES)
        if form.is_valid():
            candidat_profile, created = Candidat.objects.get_or_create(user=request.user)
            if form.cleaned_data['cv']:
                candidat_profile.cv = form.cleaned_data['cv']
            if form.cleaned_data['lettres_motivation']:
                candidat_profile.lettres_motivation = form.cleaned_data['lettres_motivation']
            candidat_profile.competences = form.cleaned_data['competences']
            candidat_profile.save()
            return redirect('profile')
    else:
        form = CandidatForm()
    return render(request, 'upload_resume.html', {'form': form})

def search_job_offers(request):
    """Recherche des offres d'emploi basées sur un critère."""
    query = request.GET.get('q')
    if query:
        job_offers = JobOffer.objects.filter(titre__icontains=query) | JobOffer.objects.filter(description__icontains=query)
    else:
        job_offers = JobOffer.objects.all()

    return render(request, 'search_job_offers.html', {
        'job_offers': job_offers,
        'query': query
    })
    
# @login_required
# def postuler_offre(request, offre_id):
#     """Permettre à un candidat de postuler à une offre d'emploi."""
#     offre = get_object_or_404(JobOffer, id=offre_id)

#     if request.method == 'POST':
#         candidature = Candidature(candidat=request.user.candidat_profile, offre=offre)
#         candidature.save()
#         return redirect('job_list')  # Rediriger vers la liste des offres après la candidature

#     return render(request, 'postuler_offre.html', {'offre': offre})
# @login_required
# def postuler_offre(request, offre_id):
#     """Permettre à un candidat de postuler à une offre d'emploi."""
#     offre = get_object_or_404(JobOffer, id=offre_id)

#     if request.method == 'POST':
#         candidature = Candidature(candidat=request.user.candidat_profile, offre=offre)
#         candidature.save()
#         return redirect('job_list')  # Rediriger vers la liste des offres après la candidature

#     return render(request, 'postuler_offre.html', {'offre': offre})
@login_required
def postuler_offre(request, offre_id):
    """Permettre à un candidat de postuler à une offre d'emploi avec un CV et une lettre de motivation."""
    offre = get_object_or_404(JobOffer, id=offre_id)
    allowed_extensions = ['pdf', 'doc', 'docx']  # Extensions autorisées, sans le point

    if request.method == 'POST':
        cv = request.FILES.get('cv')
        lettre_motivation = request.FILES.get('lettre_motivation')

        # Vérification que les fichiers sont bien présents
        if cv and lettre_motivation:
            # Extraction de l'extension de chaque fichier
            cv_extension = os.path.splitext(cv.name)[1][1:].lower()  # Retire le point et met en minuscule
            lettre_extension = os.path.splitext(lettre_motivation.name)[1][1:].lower()

            # Validation des extensions
            if cv_extension in allowed_extensions and lettre_extension in allowed_extensions:
                # Sauvegarde de la candidature si les extensions sont valides
                candidature = Candidature(
                    candidat=request.user,
                    offre=offre,
                    cv=cv,
                    lettre_motivation=lettre_motivation
                )
                candidature.save()
                
                # Message de succès
                messages.success(request, "Votre candidature a été soumise avec succès.")
                
                return redirect('job_list')  # Redirige vers la liste des offres après la candidature
            else:
                # Affiche un message d'erreur si les extensions sont incorrectes
                messages.error(request, "Veuillez télécharger des fichiers au format .pdf, .doc ou .docx uniquement.")
                return render(request, 'postuler_offre.html', {'offre': offre})

        else:
            messages.error(request, "Veuillez télécharger le CV et la lettre de motivation.")
            return render(request, 'postuler_offre.html', {'offre': offre})

    return render(request, 'postuler_offre.html', {'offre': offre})

@login_required
def mes_candidatures(request):
    """Afficher toutes les candidatures pour les offres d'emploi du recruteur."""
    # Obtenir le recruteur correspondant à l'utilisateur connecté
    try:
        recruteur = Recruteur.objects.get(user=request.user)
    except Recruteur.DoesNotExist:
        # Gérer le cas où l'utilisateur n'est pas un recruteur
        return render(request, 'error_page.html', {'message': "Vous n'êtes pas un recruteur."})

    # Filtrer les offres créées par le recruteur
    offres = JobOffer.objects.filter(recruteur=recruteur)
    candidatures = Candidature.objects.filter(offre__in=offres)
    
    return render(request, 'mes_candidatures.html', {'candidatures': candidatures})
    
def job_detail(request, offre_id):
    """Afficher les détails d'une offre d'emploi."""
    offre = get_object_or_404(JobOffer, id=offre_id)

    return render(request, 'job_detail.html', {'offre': offre})

def about_view(request):
    sections = [
        {
            'title': 'Accessibilité pour tous',
            'icon': 'fas fa-wheelchair',
            'image': 'images/Transportation_For_All.jpg',
            'text': 'Nous visons à rendre la mobilité accessible pour tout le monde, y compris les personnes ayant des conditions qui ne leur permettent pas de se déplacer facilement.'
        },
        # Add more sections here...
    ]
    return render(request, 'about.html', {'sections': sections})
