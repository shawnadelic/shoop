# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from enumfields import Enum, EnumIntegerField
from polymorphic.models import PolymorphicModel

from shuup.campaigns.utils import get_product_ids_and_quantities
from shuup.core.fields import MoneyValueField
from shuup.core.models import Category, Contact, ContactGroup, Product
from shuup.utils.properties import MoneyPropped, PriceProperty


class CartCondition(PolymorphicModel):
    model = None
    active = models.BooleanField(default=True)
    name = _("Cart condition")

    def matches(self, cart, lines):
        return False

    def __str__(self):
        return force_text(self.name)


class CartTotalProductAmountCondition(CartCondition):
    identifier = "cart_product_condition"
    name = _("Cart product count")

    product_count = models.DecimalField(
        verbose_name=_("product count in cart"), blank=True, null=True, max_digits=36, decimal_places=9)

    def matches(self, cart, lines):
        return (cart.product_count >= self.product_count)

    @property
    def description(self):
        return _("Limit the campaign to match when cart has at least the product count entered here.")

    @property
    def value(self):
        return self.product_count

    @value.setter
    def value(self, value):
        self.product_count = value


class CartTotalAmountCondition(MoneyPropped, CartCondition):
    identifier = "cart_amount_condition"
    name = _("Cart total value")

    amount = PriceProperty("amount_value", "campaign.shop.currency", "campaign.shop.prices_include_tax")
    amount_value = MoneyValueField(default=None, blank=True, null=True, verbose_name=_("cart total amount"))

    def matches(self, cart, lines):
        return (cart.total_price_of_products.value >= self.amount_value)

    @property
    def description(self):
        return _("Limit the campaign to match when it has at least the total value entered here worth of products.")

    @property
    def value(self):
        return self.amount_value

    @value.setter
    def value(self, value):
        self.amount_value = value


class CartMaxTotalProductAmountCondition(CartCondition):
    identifier = "cart_max_product_condition"
    name = _("Cart maximum product count")

    product_count = models.DecimalField(
        verbose_name=_("maximum product count in cart"), blank=True, null=True, max_digits=36, decimal_places=9)

    def matches(self, cart, lines):
        return (cart.product_count <= self.product_count)

    @property
    def description(self):
        return _("Limit the campaign to match when cart has at maximum the product count entered here.")

    @property
    def value(self):
        return self.product_count

    @value.setter
    def value(self, value):
        self.product_count = value


class CartMaxTotalAmountCondition(MoneyPropped, CartCondition):
    identifier = "cart_max_amount_condition"
    name = _("Cart maximum total value")

    amount = PriceProperty("amount_value", "campaign.shop.currency", "campaign.shop.prices_include_tax")
    amount_value = MoneyValueField(default=None, blank=True, null=True, verbose_name=_("maximum cart total amount"))

    def matches(self, cart, lines):
        return (cart.total_price_of_products.value <= self.amount_value)

    @property
    def description(self):
        return _("Limit the campaign to match when it has at maximum the total value entered here worth of products.")

    @property
    def value(self):
        return self.amount_value

    @value.setter
    def value(self, value):
        self.amount_value = value


class ComparisonOperator(Enum):
    EQUALS = 0
    GTE = 1

    class Labels:
        EQUALS = _('Exactly')
        GTE = _('Greater than or equal to')


class ProductsInCartCondition(CartCondition):
    identifier = "cart_products_condition"
    name = _("Products in cart")

    model = Product

    operator = EnumIntegerField(
        ComparisonOperator, default=ComparisonOperator.GTE, verbose_name=_("operator"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    products = models.ManyToManyField(Product, verbose_name=_("products"), blank=True)

    def matches(self, cart, lines):
        product_id_to_qty = get_product_ids_and_quantities(cart)
        product_ids = self.products.filter(id__in=product_id_to_qty.keys()).values_list("id", flat=True)
        for product_id in product_ids:
            if self.operator == ComparisonOperator.GTE:
                return product_id_to_qty[product_id] >= self.quantity
            elif self.operator == ComparisonOperator.EQUALS:
                return product_id_to_qty[product_id] == self.quantity
        return False

    @property
    def description(self):
        return _("Limit the campaign to have the selected products in cart.")

    @property
    def values(self):
        return self.products

    @values.setter
    def values(self, value):
        self.products = value


class ContactGroupCartCondition(CartCondition):
    model = ContactGroup
    identifier = "cart_contact_group_condition"
    name = _("Contact Group")

    contact_groups = models.ManyToManyField(ContactGroup, verbose_name=_("contact groups"))

    def matches(self, cart, lines=[]):
        contact_group_ids = cart.customer.groups.values_list("pk", flat=True)
        return self.contact_groups.filter(pk__in=contact_group_ids).exists()

    @property
    def description(self):
        return _("Limit the campaign to members of the selected contact groups.")

    @property
    def values(self):
        return self.contact_groups

    @values.setter
    def values(self, values):
        self.contact_groups = values


class ContactCartCondition(CartCondition):
    model = Contact
    identifier = "cart_contact_condition"
    name = _("Contact")

    contacts = models.ManyToManyField(Contact, verbose_name=_("contacts"))

    def matches(self, cart, lines=[]):
        customer = cart.customer
        return bool(customer and self.contacts.filter(pk=customer.pk).exists())

    @property
    def description(self):
        return _("Limit the campaign to selected contacts.")

    @property
    def values(self):
        return self.contacts

    @values.setter
    def values(self, values):
        self.contacts = values


class CategoryProductsCartCondition(CartCondition):
    identifier = "cart_category_condition"
    name = _("Category products in cart")

    operator = EnumIntegerField(
        ComparisonOperator, default=ComparisonOperator.GTE, verbose_name=_("operator"))
    quantity = models.PositiveIntegerField(default=1, verbose_name=_("quantity"))
    category = models.ForeignKey(Category, verbose_name=_("category"), blank=True)

    def matches(self, cart, lines):
        product_id_to_qty = get_product_ids_and_quantities(cart)
        category_product_ids = self.category.shop_products.filter(
            product_id__in=product_id_to_qty.keys()
        ).values_list(
            "product_id", flat=True
        )
        product_count = sum(product_id_to_qty[product_id] for product_id in category_product_ids)
        if self.operator == ComparisonOperator.EQUALS:
            return bool(product_count == self.quantity)
        else:
            return bool(product_count >= self.quantity)

    @property
    def description(self):
        return _("Limit the campaign to match the products from selected category.")
