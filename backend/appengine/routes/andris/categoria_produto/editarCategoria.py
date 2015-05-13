from __future__ import absolute_import, unicode_literals

from __future__ import absolute_import, unicode_literals
from categoria_produto.categoria_produtoM import CategoriaForm, Categoria
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse

from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

@login_not_required
@no_csrf
def editarCategoria(categoria_id,nomeCategoria):
    categoria = Categoria.get_by_id(int(categoria_id))
    categoria.nomeCategoria = nomeCategoria
    categoria.put()
    from routes.andris import admin
    return RedirectResponse(admin)

