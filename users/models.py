from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', _('Administrateur')
        OPC = 'OPC', _('Ordonnanceur Pilote Coordinateur')
        MAITRE_OUVRAGE = 'MAITRE_OUVRAGE', _('Maître d\'ouvrage')
        ENTREPRENEUR = 'ENTREPRENEUR', _('Entrepreneur')
        SOUS_TRAITANT = 'SOUS_TRAITANT', _('Sous-traitant')

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.OPC,
        verbose_name=_('Rôle')
    )
    company = models.CharField(max_length=100, blank=True, verbose_name=_('Entreprise'))
    phone = models.CharField(max_length=20, blank=True, verbose_name=_('Téléphone'))
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
        if self.role not in dict(self.Role.choices):
            raise ValidationError({
                'role': _('Le rôle sélectionné n\'est pas valide.')
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_opc(self):
        return self.role == self.Role.OPC

    @property
    def is_maitre_ouvrage(self):
        return self.role == self.Role.MAITRE_OUVRAGE

    @property
    def is_entrepreneur(self):
        return self.role == self.Role.ENTREPRENEUR

    @property
    def is_sous_traitant(self):
        return self.role == self.Role.SOUS_TRAITANT
