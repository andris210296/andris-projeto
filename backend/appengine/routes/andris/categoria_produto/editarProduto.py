from __future__ import absolute_import, unicode_literals

from __future__ import absolute_import, unicode_literals
from categoria_produto.categoria_produtoM import ProdutoForm,Produto
from gaecookie.decorator import no_csrf
from config.template_middleware import TemplateResponse

from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path


from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required

@login_not_required
@no_csrf
def editarProduto(produto_id,nomeProduto,precoProduto):
    produto = Produto.get_by_id(int(produto_id))
    produto.nomeProduto = nomeProduto
    produto.precoProduto = precoProduto
    produto.put()
    from routes.andris import admin
    return RedirectResponse(admin)

