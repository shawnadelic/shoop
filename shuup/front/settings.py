# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.

#: Spec string for the class used for creating Order from a Cart.
#:
#: This is the easiest way to customize the order creation process
#: without having to override a single URL or touch the ``shuup.front`` code.
SHUUP_BASKET_ORDER_CREATOR_SPEC = (
    "shuup.front.cart.order_creator:CartOrderCreator")

#: Spec string for the Django CBV (or an API-compliant class) for the cart view.
#:
#: This view deals with ``/cart/``.
SHUUP_BASKET_VIEW_SPEC = (
    "shuup.front.views.cart:DefaultCartView")

#: Spec string for the command dispatcher used when products are added/deleted/etc.
#: from the cart.
#:
#: This view deals with commands ``POST``ed to ``/cart/``.
SHUUP_BASKET_COMMAND_DISPATCHER_SPEC = (
    "shuup.front.cart.command_dispatcher:CartCommandDispatcher")

#: Spec string for the update method dispatcher used when the cart is updated (usually
#: on the cart page).
SHUUP_BASKET_UPDATE_METHODS_SPEC = (
    "shuup.front.cart.update_methods:CartUpdateMethods")

#: Spec string for the cart class used in the frontend.
#:
#: This is used to customize the behavior of the cart for a given installation,
#: for instance to modify prices of products based on certain conditions, etc.
SHUUP_BASKET_CLASS_SPEC = (
    "shuup.front.cart.objects:BaseCart")

#: The spec string defining which cart storage class to use for the frontend.
#:
#: Cart storages are responsible for persisting visitor cart state, whether
#: in the database (DatabaseCartStorage) or directly in the session
#: (DirectSessionCartStorage).  Custom storage backends could use caches, flat
#: files, etc. if required.
SHUUP_BASKET_STORAGE_CLASS_SPEC = (
    "shuup.front.cart.storage:DatabaseCartStorage")

#: Spec string for the Django CBV (or an API-compliant class) for the checkout view.
#:
#: This is used to customize the behavior of the checkout process; most likely to
#: switch in a view with a different ``phase_specs``.
SHUUP_CHECKOUT_VIEW_SPEC = (
    "shuup.front.views.checkout:DefaultCheckoutView")

#: Whether Shuup uses its own error handlers.
#:
#: If this value is set to ``False`` django defaults are used or the ones specified
#: in ``settings.ROOT_URLCONF`` file.
#:
#: Setting this to ``True`` won't override handlers specified
#: in ``settings.ROOT_URLCONF``.
#:
#: Handled error cases are: 400, 403, 404, and 500
SHUUP_FRONT_INSTALL_ERROR_HANDLERS = True

#: A dictionary defining properties to override the default field properties of the
#: checkout address form. Should map the field name (as a string) to a dictionary
#: containing the overridding Django form field properties, as in the following
#: example which makes the postal code a required field:
#:
#: SHUUP_FRONT_ADDRESS_FIELD_PROPERTIES = {
#:    "postal_code": {"required": True}
#: }
#:
#: It should be noted, however, that overriding some settings (such as making a
#: required field non-required) could create other validation issues.
SHUUP_FRONT_ADDRESS_FIELD_PROPERTIES = {}
