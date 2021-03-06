# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from shuup.admin.base import AdminModule, MenuEntry
from shuup.admin.menu import PRODUCTS_MENU_CATEGORY
from shuup.admin.utils.permissions import get_default_model_permissions
from shuup.admin.utils.urls import derive_model_url, get_edit_and_list_urls
from shuup.core.models import SalesUnit


class SalesUnitModule(AdminModule):
    name = _("Sales Units")
    breadcrumbs_menu_entry = MenuEntry(name, url="shuup_admin:sales_unit.list")

    def get_urls(self):
        return get_edit_and_list_urls(
            url_prefix="^sales-units",
            view_template="shuup.admin.modules.sales_units.views.SalesUnit%sView",
            name_template="sales_unit.%s",
            permissions=get_default_model_permissions(SalesUnit)
        )

    def get_menu_entries(self, request):
        return [
            MenuEntry(
                text=self.name,
                icon="fa fa-asterisk",
                url="shuup_admin:sales_unit.list",
                category=PRODUCTS_MENU_CATEGORY,
                ordering=5
            ),
        ]

    def get_required_permissions(self):
        return get_default_model_permissions(SalesUnit)

    def get_model_url(self, object, kind):
        return derive_model_url(SalesUnit, "shuup_admin:sales_unit", object, kind)
