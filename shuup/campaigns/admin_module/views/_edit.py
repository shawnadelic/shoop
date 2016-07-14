# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.db.transaction import atomic
from django.utils.translation import ugettext_lazy as _

from shuup.admin.form_part import FormPartsViewMixin, SaveFormPartsMixin
from shuup.admin.toolbar import get_default_edit_toolbar
from shuup.admin.utils.views import CreateOrUpdateView
from shuup.apps.provides import get_provide_objects
from shuup.campaigns.admin_module.form_parts import (
    CartBaseFormPart, CartConditionsFormPart,
    CartDiscountEffectsFormPart, CartLineEffectsFormPart,
    CatalogBaseFormPart, CatalogConditionsFormPart, CatalogEffectsFormPart,
    CatalogFiltersFormPart
)
from shuup.campaigns.admin_module.forms import CouponForm
from shuup.campaigns.models.campaigns import (
    CartCampaign, CatalogCampaign, Coupon
)
from shuup.campaigns.utils import _Breadcrumbed


class CampaignEditView(SaveFormPartsMixin, FormPartsViewMixin, CreateOrUpdateView):
    template_name = "shuup/campaigns/admin/edit_campaigns.jinja"
    context_object_name = "campaign"
    form_part_class_provide_key = "campaign"
    add_form_errors_as_messages = False
    rules_form_part_class = None  # Override in subclass
    effects = []  # Override in subclass
    condition_key = ""  # Override in subclass

    @atomic
    def form_valid(self, form):
        return self.save_form_parts(form)

    def get_form_parts(self, object):
        form_parts = super(CampaignEditView, self).get_form_parts(object)
        if not object.pk:
            return form_parts

        for form in get_provide_objects(self.condition_key):
            form_parts.append(self._get_rules_form_part(form, object))

        for provide_key, form_part_class in self.effects:
            for form in get_provide_objects(provide_key):
                form_parts.append(self._get_effects_form_part(form, object, form_part_class))

        return form_parts

    def _get_rules_form_part(self, form, object):
        return self.rules_form_part_class(
            self.request, form, "conditions_%s" % form._meta.model.__name__.lower(), object)

    def _get_effects_form_part(self, form, object, cls):
        return cls(self.request, form, "effects_%s" % form._meta.model.__name__.lower(), object)

    def get_toolbar(self):
        save_form_id = self.get_save_form_id()
        return get_default_edit_toolbar(self, save_form_id)


class CatalogCampaignEditView(_Breadcrumbed, CampaignEditView):
    model = CatalogCampaign
    condition_key = "campaign_context_condition"
    filter_key = "campaign_catalog_filter"
    effects = [("campaign_product_discount_effect_form", CatalogEffectsFormPart)]
    base_form_part_classes = [CatalogBaseFormPart]
    rules_form_part_class = CatalogConditionsFormPart

    parent_name = _("Catalog Campaign")
    parent_url = "shuup_admin:catalog_campaigns.list"

    def get_form_parts(self, object):
        form_parts = super(CatalogCampaignEditView, self).get_form_parts(object)
        if not object.pk:
            return form_parts

        for form in get_provide_objects(self.filter_key):
            form_parts.append(self._get_filters_form_part(form, object))

        return form_parts

    def _get_filters_form_part(self, form, object):
        return CatalogFiltersFormPart(
            self.request, form, "filters_%s" % form._meta.model.__name__.lower(), object)


class CartCampaignEditView(_Breadcrumbed, CampaignEditView):
    model = CartCampaign
    condition_key = "campaign_cart_condition"
    effects = [
        ("campaign_cart_discount_effect_form", CartDiscountEffectsFormPart),
        ("campaign_cart_line_effect_form", CartLineEffectsFormPart)
    ]
    base_form_part_classes = [CartBaseFormPart]
    rules_form_part_class = CartConditionsFormPart

    parent_name = _("Cart Campaign")
    parent_url = "shuup_admin:cart_campaigns.list"


class CouponEditView(_Breadcrumbed, CreateOrUpdateView):
    model = Coupon
    template_name = "shuup/campaigns/admin/edit_coupons.jinja"
    form_class = CouponForm
    context_object_name = "coupon"
    add_form_errors_as_messages = True
    parent_name = _("Coupon")
    parent_url = "shuup_admin:coupons.list"
