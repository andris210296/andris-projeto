# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria.categoriaM import CategoriaForm, Categoria

from config.template_middleware import TemplateResponse

from tekton.gae.middleware.redirect import RedirectResponse


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
        contexto = {'categoria':campos,'erros':erros}
        return TemplateResponse(contexto,template_path='/andris/admin.html')