from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        # Création d'un utilisateur OPC de test
        self.opc_user = User.objects.create_user(
            username='opc_user',
            email='opc@example.com',
            password='testpass123',
            first_name='John',
            last_name='Doe',
            role=User.Role.OPC,
            company='Test Company',
            phone='0123456789'
        )

        # Création d'un utilisateur Maître d'ouvrage de test
        self.maitre_ouvrage = User.objects.create_user(
            username='mo_user',
            email='mo@example.com',
            password='testpass123',
            first_name='Jane',
            last_name='Smith',
            role=User.Role.MAITRE_OUVRAGE,
            company='MO Company'
        )

    def test_user_creation(self):
        """Test la création basique d'un utilisateur"""
        self.assertEqual(self.opc_user.username, 'opc_user')
        self.assertEqual(self.opc_user.email, 'opc@example.com')
        self.assertEqual(self.opc_user.get_full_name(), 'John Doe')
        self.assertTrue(self.opc_user.is_active)
        self.assertFalse(self.opc_user.is_staff)
        self.assertFalse(self.opc_user.is_superuser)

    def test_user_roles(self):
        """Test les différents rôles d'utilisateur"""
        self.assertEqual(self.opc_user.role, User.Role.OPC)
        self.assertEqual(self.maitre_ouvrage.role, User.Role.MAITRE_OUVRAGE)
        self.assertEqual(str(self.opc_user.get_role_display()), 'Ordonnanceur Pilote Coordinateur')
        self.assertEqual(str(self.maitre_ouvrage.get_role_display()), 'Maître d\'ouvrage')

    def test_role_properties(self):
        """Test les propriétés de rôle"""
        self.assertTrue(self.opc_user.is_opc)
        self.assertFalse(self.opc_user.is_maitre_ouvrage)
        self.assertFalse(self.opc_user.is_entrepreneur)
        self.assertFalse(self.opc_user.is_sous_traitant)

        self.assertTrue(self.maitre_ouvrage.is_maitre_ouvrage)
        self.assertFalse(self.maitre_ouvrage.is_opc)
        self.assertFalse(self.maitre_ouvrage.is_entrepreneur)
        self.assertFalse(self.maitre_ouvrage.is_sous_traitant)

    def test_user_string_representation(self):
        """Test la représentation en chaîne de caractères de l'utilisateur"""
        expected_opc = 'John Doe (Ordonnanceur Pilote Coordinateur)'
        expected_mo = 'Jane Smith (Maître d\'ouvrage)'
        self.assertEqual(str(self.opc_user), expected_opc)
        self.assertEqual(str(self.maitre_ouvrage), expected_mo)

    def test_user_company_and_phone(self):
        """Test les champs company et phone"""
        self.assertEqual(self.opc_user.company, 'Test Company')
        self.assertEqual(self.opc_user.phone, '0123456789')
        self.assertEqual(self.maitre_ouvrage.company, 'MO Company')
        self.assertEqual(self.maitre_ouvrage.phone, '')

    def test_create_superuser(self):
        """Test la création d'un superutilisateur"""
        admin = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_active)

    def test_invalid_role(self):
        """Test la validation du rôle"""
        with self.assertRaises(ValidationError):
            User.objects.create_user(
                username='invalid_user',
                email='invalid@example.com',
                password='testpass123',
                role='INVALID_ROLE'
            )

    def test_user_timestamps(self):
        """Test les champs de timestamp"""
        self.assertIsNotNone(self.opc_user.created_at)
        self.assertIsNotNone(self.opc_user.updated_at)
        self.assertIsNotNone(self.opc_user.date_joined)
