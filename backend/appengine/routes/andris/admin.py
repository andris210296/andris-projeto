# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.andris.categoria_produto.categoria_produtoM import Produto,Categoria
from tekton import router
from gaepermission.decorator import login_not_required
from routes.andris.categoria_produto.ngCategoria import salvarCategoria,listarCategoria,deletarCategoria,editarCategoria


#@permissions(ADMIN)
@no_csrf
@login_not_required
def index():

    categoria_query = Categoria.query_ordenada_por_nome()
    produto_query = Produto.query_ordenada_por_nome()

    categorias = categoria_query.fetch()
    produtos = produto_query.fetch()



    for cat in categorias:
        cat_key = cat.key
        cat_key_id = cat_key.id()

        cat.QtdProd = len(Produto.query_por_categoria_ordenada_por_nome(Categoria.get_by_id(int(cat_key_id))).fetch())

    for prod in produtos:
        prod_key = prod.key
        prod_key_id = prod_key.id()




    # Angular
    salvar_path = router.to_path(salvarCategoria)   #Agora que está sendo utilizado o angular, o path foi para um arquivo diferente, pois nele há json

    listar_path = router.to_path(listarCategoria)

    deletar_path = router.to_path(deletarCategoria)

    editar_path = router.to_path(editarCategoria)




    contexto = {'categoria_lista':categorias,
                'rest_salvar_path':salvar_path,'rest_list_path':listar_path,
                'rest_delete_path':deletar_path,'rest_edit_path':editar_path}

    return TemplateResponse(contexto,template_path='/andris/admin.html')






