from __future__ import absolute_import, unicode_literals
from google.appengine.ext import ndb
from unittest import TestCase
from config.template_middleware import TemplateResponse
from base import GAETestCase
from routes.andris.categoria_produto.categoria_produtoM import Categoria,CategoriaForm
from routes.andris.categoria_produto import ngCategoria
import json
from tekton.gae.middleware.redirect import RedirectResponse

class ExemploTest(GAETestCase):
    def test_salvarCategoria(self):

        qtd_antes = len(Categoria.query().fetch())
        nova_categoria = ngCategoria.salvar(nomeCategoria='testCategoria')

        qtd_depois = len(Categoria.query().fetch())

        self.assertEquals(qtd_antes+1,qtd_depois)
        self.assertEquals('testCategoria',Categoria.query().fetch()[0].nomeCategoria)

    def test_validacao(self):
        nova_categoria = ngCategoria.salvar()
        self.assertIsInstance(nova_categoria, TemplateResponse)
        self.assertIsNone(Categoria.query().get())
        self.maxDiff = True
        self.assertDictEqual({u'categoria': {}, u'erros': {'nomeCategoria': u'Required field'}}, nova_categoria.context)





