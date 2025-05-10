from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class User(AbstractUser):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrateur'),
        ('MANAGER', 'Gestionnaire'),
        ('USER', 'Utilisateur'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='USER')
    company = models.CharField(max_length=100, blank=True, verbose_name=_('Entreprise'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Téléphone'))
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name=_('Actif'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Créé le'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Mis à jour le'))

    class Meta:
        verbose_name = _('Utilisateur')
        verbose_name_plural = _('Utilisateurs')

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def clean(self):
        super().clean()
        if self.role not in dict(self.ROLE_CHOICES):
            raise ValidationError({'role': 'Rôle invalide'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_opc(self):
        return self.role == 'ADMIN'

    @property
    def is_maitre_ouvrage(self):
        return self.role == 'ADMIN'

    @property
    def is_entrepreneur(self):
        return self.role == 'ADMIN'

    @property
    def is_sous_traitant(self):
        return self.role == 'ADMIN'

    def get_profile_picture_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return '/static/images/default-avatar.png'
