from __future__ import absolute_import, unicode_literals

from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from categoria.categoriaM import *
from routes.andris.admin import *
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


@no_csrf
def index(categoria_id):
    categoria=Categoria.get_by_id(int(categoria_id))
    ctx={'categoria':categoria,
         'salvar_path': to_path(atualizar)}
    return TemplateResponse(ctx,'andris/admin.html')

def atualizar(categoria_id,nomeCategoria):
    categoria = Categoria.get_by_id(int(categoria_id))
    categoria.nomeCategoria = nomeCategoria
    categoria.put()
    return RedirectResponse()