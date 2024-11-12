# app/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Recruteur, Candidat

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'RECRUTEUR':
            Recruteur.objects.create(user=instance)
        elif instance.role == 'CANDIDAT':
            Candidat.objects.create(user=instance)
