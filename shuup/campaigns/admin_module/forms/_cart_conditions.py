# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from shuup.campaigns.models.cart_conditions import (
    CartMaxTotalAmountCondition, CartMaxTotalProductAmountCondition,
    CartTotalAmountCondition, CartTotalProductAmountCondition,
    CategoryProductsCartCondition, ContactCartCondition,
    ContactGroupCartCondition, ProductsInCartCondition
)

from ._base import BaseRuleModelForm


class CartTotalProductAmountConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = CartTotalProductAmountCondition


class CartTotalAmountConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = CartTotalAmountCondition


class ProductsInCartConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = ProductsInCartCondition


class ContactGroupCartConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = ContactGroupCartCondition


class ContactCartConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = ContactCartCondition


class CartMaxTotalProductAmountConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = CartMaxTotalProductAmountCondition


class CartMaxTotalAmountConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = CartMaxTotalAmountCondition


class CategoryProductsCartConditionForm(BaseRuleModelForm):
    class Meta(BaseRuleModelForm.Meta):
        model = CategoryProductsCartCondition
