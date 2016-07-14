# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
import decimal
import pytest

from shuup.campaigns.models import CartCampaign
from shuup.campaigns.models.cart_conditions import (
    CategoryProductsCartCondition, ComparisonOperator
)
from shuup.campaigns.models.cart_line_effects import (
    DiscountFromCategoryProducts
)
from shuup.front.cart import get_cart
from shuup.testing.factories import create_product, get_default_supplier, get_default_category
from shuup_tests.campaigns import initialize_test


@pytest.mark.django_db
def test_category_product_in_cart_condition(rf):
    request, shop, group = initialize_test(rf, False)
    cart = get_cart(request)
    supplier = get_default_supplier()
    category = get_default_category()
    product = create_product("The Product", shop=shop, default_price="200")
    cart.add_product(supplier=supplier, shop=shop, product=product, quantity=1)

    shop_product = product.get_shop_instance(shop)
    assert category not in shop_product.categories.all()

    condition = CategoryProductsCartCondition.objects.create(
        category=category, operator=ComparisonOperator.EQUALS, quantity=1)

    # No match the product does not have the category
    assert not condition.matches(cart, [])

    shop_product.categories.add(category)
    assert condition.matches(cart, [])

    cart.add_product(supplier=supplier, shop=shop, product=product, quantity=1)
    assert not condition.matches(cart, [])

    condition.operator = ComparisonOperator.GTE
    condition.save()

    assert condition.matches(cart, [])


@pytest.mark.django_db
def test_category_products_effect_with_amount(rf):
    request, shop, group = initialize_test(rf, False)

    cart = get_cart(request)
    category = get_default_category()
    supplier = get_default_supplier()

    single_product_price = "50"
    discount_amount_value = "10"
    quantity = 5

    product = create_product("The product", shop=shop, supplier=supplier, default_price=single_product_price)
    shop_product = product.get_shop_instance(shop)
    shop_product.categories.add(category)

    cart.add_product(supplier=supplier, shop=shop, product=product, quantity=quantity)
    cart.save()

    rule = CategoryProductsCartCondition.objects.create(
        category=category, operator=ComparisonOperator.EQUALS, quantity=quantity)

    campaign = CartCampaign.objects.create(active=True, shop=shop, name="test", public_name="test")
    campaign.conditions.add(rule)

    DiscountFromCategoryProducts.objects.create(
        campaign=campaign, category=category, discount_amount=discount_amount_value)

    assert rule.matches(cart, [])
    cart.uncache()
    final_lines = cart.get_final_lines()

    assert len(final_lines) == 1  # no new lines since the effect touches original lines
    expected_discount_amount = quantity * cart.create_price(discount_amount_value)
    original_price = cart.create_price(single_product_price) * quantity
    line = final_lines[0]
    assert line.discount_amount == expected_discount_amount
    assert cart.total_price == original_price - expected_discount_amount


@pytest.mark.django_db
def test_category_products_effect_with_percentage(rf):
    request, shop, group = initialize_test(rf, False)

    cart = get_cart(request)
    category = get_default_category()
    supplier = get_default_supplier()

    single_product_price = "50"
    discount_percentage = decimal.Decimal("0.10")
    quantity = 5

    product = create_product("The product", shop=shop, supplier=supplier, default_price=single_product_price)
    shop_product = product.get_shop_instance(shop)
    shop_product.categories.add(category)

    cart.add_product(supplier=supplier, shop=shop, product=product, quantity=quantity)
    cart.save()

    rule = CategoryProductsCartCondition.objects.create(
        category=category, operator=ComparisonOperator.EQUALS, quantity=quantity)

    campaign = CartCampaign.objects.create(active=True, shop=shop, name="test", public_name="test")
    campaign.conditions.add(rule)

    DiscountFromCategoryProducts.objects.create(
        campaign=campaign, category=category, discount_percentage=discount_percentage)

    assert rule.matches(cart, [])
    cart.uncache()
    final_lines = cart.get_final_lines()

    assert len(final_lines) == 1  # no new lines since the effect touches original lines
    expected_discount_amount = quantity * cart.create_price(single_product_price) * discount_percentage
    original_price = cart.create_price(single_product_price) * quantity
    line = final_lines[0]
    assert line.discount_amount == expected_discount_amount
    assert cart.total_price == original_price - expected_discount_amount
