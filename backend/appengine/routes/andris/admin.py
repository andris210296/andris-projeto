# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.andris.categoria_produto.categoria_produtoM import Produto,Categoria
from tekton import router
from gaepermission.decorator import login_not_required
from routes.andris.categoria_produto.ngCategoria import salvarCategoria,listarCategoria,deletarCategoria,editarCategoria
from routes.andris import updown
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from blob_app import blob_facade

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






    upload_path = router.to_path(updown.upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(upload_path, gs_bucket_name=bucket)



    comando = blob_facade.list_blob_files_cmd()
    arquivos = comando()
    download_path= router.to_path(updown.download)
    for arq in arquivos:
        arq.download_path=router.to_path(download_path,arq.key.id(),arq.filename)


    contexto = {'categoria_lista':categorias,'upload_path':url,'arquivos':arquivos,
                'rest_salvar_path':salvar_path,'rest_list_path':listar_path,
                'rest_delete_path':deletar_path,'rest_edit_path':editar_path}

    return TemplateResponse(contexto,template_path='/andris/admin.html')






