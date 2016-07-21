# -*- coding: utf-8 -*-
# This file is part of Shuup.
#
# Copyright (c) 2012-2016, Shoop Ltd. All rights reserved.
#
# This source code is licensed under the AGPLv3 license found in the
# LICENSE file in the root directory of this source tree.
from django.db import IntegrityError
from django.http.response import JsonResponse
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View

from shuup.admin.utils.urls import get_model_url
from shuup.core.models import Product


class ProductDuplicateView(View):
    """
    Create a duplicate of a product.
    """
    def post(self, request, *args, **kwargs):
        parent = Product.objects.get(id=request.POST["id"])
        sku = request.POST["sku"]
        name_suffix = request.POST.get("name_suffix", None)
        try:
            duplicate = parent.create_duplicate(sku, name_suffix)
            return JsonResponse({
                "text": duplicate.name,
                "id": duplicate.id,
                "url": get_model_url(duplicate),
            })
        except IntegrityError:
            return JsonResponse({
                "error": force_text(_("Product with SKU already exists.")),
            })
