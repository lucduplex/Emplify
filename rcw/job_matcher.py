# app/services/job_matcher.py
from app.models import JobOffer


def find_matching_jobs(competences):
    # Filtre les offres d'emploi en vérifiant si les compétences requises contiennent l'une des compétences du CV
    matching_jobs = JobOffer.objects.filter(
        competences_requises__icontains="|".join(competences)
    )
    return matching_jobs
