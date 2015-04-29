# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
from config.template_middleware import TemplateResponse
from gaecookie.decorator import no_csrf
from gaepermission.decorator import login_not_required
from categoria.categoriaM import *


@login_not_required
@no_csrf
def index():
    query = Categoria.query_ordenada_por_nome()
    contexto = {'categoria_lista':query.fetch()}
    return TemplateResponse(contexto)

