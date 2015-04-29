# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from categoria.categoria_model import Categoria
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.categorias import edit
from routes.categorias.new import salvar
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index():
    query = Categoria.query_ordenada_por_nome()
    edit_path_base = to_path(edit)
    deletar_path_base = to_path(deletar)
    categorias = query.fetch()
    for cat in categorias:
        key = cat.key
        key_id = key.id()
        cat.edit_path = to_path(edit_path_base, key_id)
        cat.deletar_path = to_path(deletar_path_base, key_id)
    ctx = {'salvar_path': to_path(salvar),
           'categorias': categorias}
    return TemplateResponse(ctx, 'categorias/categorias_home.html')


def deletar(categoria_id):
    key = ndb.Key(Categoria, int(categoria_id))
    key.delete()
    return RedirectResponse(index)