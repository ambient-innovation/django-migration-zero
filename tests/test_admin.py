from __future__ import annotations

import re
from http import HTTPStatus

from django.contrib.admin.sites import AdminSite, all_sites
from django.contrib.auth.models import User
from django.db.models import Model
from django.test import TestCase, override_settings
from django.urls import reverse
from unittest_parametrize import ParametrizedTestCase, param, parametrize

each_model_admin = parametrize(
    "site,model,model_admin",
    [
        param(
            site,
            model,
            model_admin,
            id=f"{site.name}"
            + f"{re.sub(r'(?<!^)(?=[A-Z])', '_', str(model_admin)).lower().replace('.', '_').replace('__', '_')}",
        )
        for site in all_sites
        for model, model_admin in site._registry.items()
    ],
)


@override_settings(SECURE_SSL_REDIRECT=False)
class ModelAdminTests(ParametrizedTestCase, TestCase):
    """
    Generic tests for admin "list" and "add" views.
    Source: https://adamj.eu/tech/2023/03/17/django-parameterized-tests-model-admin-classes/

    Attention: Having more than one admin class just registered without a custom class will crash the "parametrize".
    """

    user: User

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        cls.user = User.objects.create_superuser(username="admin", email="admin@example.com", password="test")

    def setUp(self):
        self.client.force_login(self.user)

    def make_url(self, site: AdminSite, model: type[Model], page: str) -> str:
        return reverse(f"{site.name}:{model._meta.app_label}_{model._meta.model_name}_{page}")

    @each_model_admin
    def test_changelist(self, site, model, model_admin):
        url = self.make_url(site, model, "changelist")
        response = self.client.get(url, {"q": "example.com"})
        assert response.status_code == HTTPStatus.OK

    @each_model_admin
    def test_add(self, site, model, model_admin):
        url = self.make_url(site, model, "add")
        response = self.client.get(url)
        self.assertIn(
            response.status_code,
            (
                HTTPStatus.OK,
                HTTPStatus.FORBIDDEN,  # some admin classes blanket disallow "add"
            ),
            f'Response "{response.status_code}" not in ({HTTPStatus.OK}, {HTTPStatus.FORBIDDEN}).',
        )
