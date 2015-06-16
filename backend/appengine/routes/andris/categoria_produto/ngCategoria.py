# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from google.appengine.ext import ndb
from tekton.gae.middleware.redirect import RedirectResponse
from routes.andris.categoria_produto.categoria_produtoM import CategoriaForm, Categoria
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.json_middleware import JsonResponse

@login_not_required
@no_csrf
def salvarCategoria(_resp,**campos):
    print campos
    categoriaForm = CategoriaForm(**campos)
    erros = categoriaForm.validate()
    if erros:
        _resp.set_status(400)
        return JsonResponse(erros)

    categoria = categoriaForm.fill_model()
    categoria.put()
    dct = categoriaForm.fill_with_model(categoria)
    return JsonResponse(dct)

@login_not_required
@no_csrf
def salvar(**kwargs):
    form= CategoriaForm(**kwargs)
    erros=form.validate()
    if not erros:
        propriedades=form.normalize()
        categoria = Categoria(**propriedades)
        categoria.put()
        from routes.andris import admin
        return RedirectResponse(admin)
    else:
        ctx = {'categoria': kwargs, 'erros':erros}
        return TemplateResponse(ctx, 'categorias/categorias_form.html')


@login_not_required
@no_csrf
def editarCategoria(_resp,**campos):
    '''
    categoriaForm = CategoriaForm(**campos)
    erros = categoriaForm.validate()
    if erros:
        _resp.set_status(400)
        return JsonResponse(erros)

    '''
    categoria_id = campos["categoria_id"]
    nomeCategoria = campos["nomeCategoria"]
    categoria = Categoria.get_by_id(int(categoria_id))
    categoria.nomeCategoria = nomeCategoria
    categoria.put()
    dct = CategoriaForm().fill_with_model(categoria)
    return JsonResponse(dct)



@login_not_required
@no_csrf
def listarCategoria():
    localized_categorias = [CategoriaForm().fill_with_model(categoria) for categoria in Categoria.query_ordenada_por_nome().fetch()]
    return JsonResponse(localized_categorias)


@login_not_required
@no_csrf
def deletarCategoria(categoria_id):
    key = ndb.Key(Categoria, int(categoria_id))
    key.delete()


