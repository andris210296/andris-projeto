# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from config.template_middleware import TemplateResponse
from gaepermission.decorator import permissions
from gaecookie.decorator import no_csrf
from categoria.categoriaM import *
from permission_app.model import ADMIN
from tekton import router
from tekton.gae.middleware.redirect import RedirectResponse
from routes.andris.categoria.salvarCategoria import salvarCategoria
from routes.andris.categoria.editarCategoria import editarCategoria


@permissions(ADMIN)
@no_csrf
def index():

    query = Categoria.query_ordenada_por_nome()
    salvar_path = router.to_path(salvarCategoria)
    editar_path = router.to_path(editarCategoria)
    deletar_path= router.to_path(deletar)
    categorias = query.fetch()

    for cat in categorias:
        key = cat.key
        key_id = key.id()
        cat.editar_path = router.to_path(editar_path)
        cat.deletar_path = router.to_path(deletar_path, key_id)


    contexto = {'categoria_lista':categorias,'salvar_path':salvar_path}
    return TemplateResponse(contexto,template_path='/andris/admin.html')

def deletar(categoria_id):
    key = ndb.Key(Categoria, int(categoria_id))
    key.delete()
    return RedirectResponse(index)






