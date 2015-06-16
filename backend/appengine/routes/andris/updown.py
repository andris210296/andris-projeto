# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from routes.andris.categoria_produto.categoria_produtoM import Produto,Categoria
from tekton import router
from gaepermission.decorator import login_not_required
from routes.andris.categoria_produto.ngCategoria import salvarCategoria,listarCategoria,deletarCategoria,editarCategoria
from google.appengine.api.app_identity.app_identity import get_default_gcs_bucket_name
from google.appengine.ext import blobstore
from blob_app import blob_facade
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from tekton.gae.middleware.redirect import RedirectResponse
from tekton.router import to_path

@no_csrf
@login_not_required

def index():
    comando = blob_facade.list_blob_files_cmd()
    arquivos = comando()
    download_path=to_path(download)
    for arq in arquivos:
        arq.download_path=to_path(download_path,arq.key.id(),arq.filename)

    ctx = {'arquivos':arquivos}

    return TemplateResponse(ctx, 'andris/admin.html')


@login_not_required
def upload(_handler, files):
    blob_infos = _handler.get_uploads('files')
    blob_facade.save_blob_files_cmd(blob_infos).execute()
    from routes.andris import admin
    return RedirectResponse(admin)



@login_not_required
@no_csrf
def download(_handler,id,filename):
    comando=blob_facade.get_blob_file_cmd(id)
    arquivo=comando()
    _handler.send_blob(arquivo.blob_key)



@login_not_required
@no_csrf
def form():
    upload_path = to_path(upload)
    bucket = get_default_gcs_bucket_name()
    url = blobstore.create_upload_url(upload_path, gs_bucket_name=bucket)
    ctx = {'upload_path': url}
    return TemplateResponse(ctx, 'andris/admin.html')