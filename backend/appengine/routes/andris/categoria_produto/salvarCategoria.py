# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria_produto.categoria_produtoM import CategoriaForm, Categoria

from config.template_middleware import TemplateResponse

from tekton.gae.middleware.redirect import RedirectResponse

from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

@login_not_required
@no_csrf
def salvarCategoria(**campos):
    categoriaForm = CategoriaForm(**campos)
    erros = categoriaForm.validate()
    if not erros:
        propriedades = categoriaForm.normalize()
        novoCat = Categoria(**propriedades)
        novoCat.put()

        from routes.andris import admin
        return RedirectResponse(admin)
    else:
        contexto = {'categoria_produto':campos,'erros':erros}
        return TemplateResponse(contexto,template_path='/andris/admin.html')