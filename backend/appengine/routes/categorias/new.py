# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from categoria.categoria_model import Categoria, CategoriaForm
from config.template_middleware import TemplateResponse
from routes import categorias
from tekton.gae.middleware.redirect import RedirectResponse


def salvar(**kwargs):
    form= CategoriaForm(**kwargs)
    erros=form.validate()
    if not erros:
        propriedades=form.normalize()
        categoria = Categoria(**propriedades)
        categoria.put()
        return RedirectResponse(categorias)
    else:
        ctx = {'categoria': kwargs, 'erros':erros}
        return TemplateResponse(ctx, 'categorias/categorias_form.html')