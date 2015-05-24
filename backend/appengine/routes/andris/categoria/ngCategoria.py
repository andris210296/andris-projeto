# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria_produto.categoria_produtoM import CategoriaForm, Categoria

from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_required, login_not_required
from tekton.gae.middleware.json_middleware import JsonResponse

@login_not_required
@no_csrf
def salvarCategoria(_resp,**campos):


    categoriaForm = CategoriaForm(**campos)


    erros = categoriaForm.validate()
    if erros:
        _resp.set_status(400)
        return JsonResponse(erros)

    categoria = categoriaForm.fill_model()
    categoria.put()
    dct = categoriaForm.fill_with_model(categoria)
    return JsonResponse(dct)