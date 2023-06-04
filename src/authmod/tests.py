from uuid import uuid4

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from faker import Faker

from accounts.tests import create_test_user
from authmod.models import Role

faker = Faker()


def create_test_permission():
    ct = ContentType.objects.get_for_model(Permission)

    return Permission.objects.create(
        name="Test Permission",
        codename=str(uuid4()),
        content_type=ct,
    )


def create_test_role():
    return Role.objects.create(name=faker.user_name())


class RoleBasedAccessTestCase(TestCase):
    def setUp(self):
        """
        This method create user, role and add permissions which
        can be used for test cases
        """
        self.user = create_test_user()
        self.role = create_test_role()

        self.user.role = self.role
        self.user.save()

        self.perm = create_test_permission()
        self.role.permissions.add(self.perm)

    def get_perm_str(self, perm):
        return f"{perm.content_type.app_label}.{perm.codename}"

    def test_check_role_perms_true(self):
        """
        Test if permission check is properly working for true case
        when assigned role to user
        """
        perm_str = self.get_perm_str(self.perm)
        self.assertTrue(self.user.has_perm(perm_str))
        self.assertTrue(self.user.has_perms([perm_str]))
        self.assertTrue(self.user.has_module_perms(self.perm.content_type.app_label))

    def test_check_user_perms_true(self):
        """
        Test if permission check is properly working for false case
        when permission assigned directly to user
        """
        perm = create_test_permission()

        self.user.user_permissions.add(perm)

        perm_str = self.get_perm_str(perm)
        self.assertTrue(self.user.has_perm(perm_str))
        self.assertTrue(self.user.has_perms([perm_str]))
        self.assertTrue(self.user.has_module_perms(perm.content_type.app_label))

    def test_check_perms_false(self):
        """
        Test if permission check is properly working for false case
        """
        perm = create_test_permission()
        perm_str = self.get_perm_str(perm)
        self.assertFalse(self.user.has_perm(perm_str))
        self.assertFalse(self.user.has_perms([perm_str]))

        ct = ContentType.objects.get_for_model(Role)
        self.assertFalse(self.user.has_module_perms(ct.app_label))

    def test_get_user_permissions(self):
        """
        Test if get user permissions is correctly working
        """
        user = create_test_user()
        perm = create_test_permission()

        user.user_permissions.add(perm)

        userperms = user.get_user_permissions()

        self.assertEquals(len(userperms), 1)

        perm_str = self.get_perm_str(perm)
        self.assertSetEqual(userperms, {perm_str})

    def test_get_role_permissions(self):
        """
        Test if get role permissions is correctly working
        """
        user = create_test_user()
        role = create_test_role()
        perm = create_test_permission()

        user.role = role
        user.save()

        role.permissions.add(perm)

        roleperms = user.get_role_permissions()

        self.assertEquals(len(roleperms), 1)

        perm_str = self.get_perm_str(perm)
        self.assertSetEqual(roleperms, {perm_str})

    def test_get_all_permissions(self):
        """
        Test if get all permissions is correctly working
        """
        user = create_test_user()
        role = create_test_role()

        user.role = role
        user.save()

        perm1 = create_test_permission()
        perm2 = create_test_permission()

        role.permissions.add(perm1)
        user.user_permissions.add(perm2)

        allperms = user.get_all_permissions()

        self.assertEquals(len(allperms), 2)

        perm_str1 = self.get_perm_str(perm1)
        perm_str2 = self.get_perm_str(perm2)

        self.assertSetEqual(allperms, {perm_str1, perm_str2})
