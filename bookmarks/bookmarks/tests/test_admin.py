"""
Tests for Django admin site pages.
"""
from django.test import (
    TestCase,
    Client,
)
from django.urls import reverse
from django.contrib import admin

from bookmarks.common.utils import (
    create_user,
    create_profile,
    create_image,
    create_action,
)


class AdminSiteTests(TestCase):
    """Tests for Django admin."""

    def setUp(self):
        self.client = Client()
        self.admin_user = create_user(superuser=True)
        self.client.force_login(user=self.admin_user)
        self.user = create_user()
        self.profile = create_profile(user=self.user)
        self.image = create_image(user=self.user)
        self.action = create_action(user=self.user)

    def test_admin_models_patterns(self):
        """
        Test all default URL patterns in admin site for each registered model.

        Tested URL patterns:
        - bookmarks_<model>_changelist
        - bookmarks_<model>_add
        - bookmarks_<model>_history
        - bookmarks_<model>_delete
        - bookmarks_<model>_change
        """
        custom_apps = ['account', 'actions', 'images']
        admin_models = []

        for admin_model in admin.site._registry.values():
            for name in custom_apps:
                if name in str(admin_model):
                    admin_models.append(admin_model)

        for model in admin_models:
            for pattern in model.get_urls():
                if pattern.name is not None:
                    model_name = str(model.opts).split('.', 1)[1]
                    model_instance = getattr(self, model_name)
                    pattern_params = [
                        'id' if 'id' in param else param
                        for param in pattern.pattern.converters
                    ]
                    url_params = [getattr(model_instance, param)
                                  for param in pattern_params]

                    if len(url_params) > 0:
                        url = reverse(f"admin:{pattern.name}", args=url_params)
                    else:
                        url = reverse(f"admin:{pattern.name}")

                    res = self.client.get(url)

                    if 'list' in pattern.name:
                        for field in model.list_of_fields:
                            self.assertContains(
                                res, getattr(model_instance, field))

                    self.assertEqual(res.status_code, 200)
