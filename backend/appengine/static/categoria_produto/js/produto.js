//https://github.com/renzon/script3manha/blob/master/backend/appengine/static/js/produtos.js

$(document).ready(function(){
    var $salvandoProdutoFlag = $('#salvandoProdutoFlag');

    $salvandoProdutoFlag.hide();

    var $nomeProdutoInput = $('#nomeProdutoInput');
    var $precoProdutoInput = $('#precoProdutoInput');
    var $categoriaIdInput = $('#categoriaIdInput');


    var $tbodyProdutos = $('#tbodyProdutos');


    function adicionarProduto(produto){

        var tr = '<tr id="tr-'+ produto.id+'">';
        tr += '<td>';
        tr +='<div class="btn-group">';

        //Input Nome Produto

        tr += '<div id="nomeProduto-div">';

        tr += '<label for="nomeProdutoInput" class="control-label"></label>';

        tr += '<div class="input-group">';
        tr += '<span class="input-group-addon">';
        tr += '<i class = "fa fa-bars"></i>';
        tr += '</span>';
        tr += '<input id="'+produto.id+'nomeProdutoInput" type = "text" class = "form-control" name="nomeProduto" value="'+produto.nomeProduto+'"/>';

        tr += '</div>';

        tr += '<span id="'+produto.id+'nomeProduto-span" class="help-block"> </span>';

        tr += '</div>';

        //Input Preço produto

        tr += '<div id="precoProduto-div">';

        tr += '<label for="precoProdutoInput" class="control-label"></label>';

        tr += '<div class="input-group">';
        tr += '<span class="input-group-addon">';
        tr += '<i class = "fa fa-money"></i>';
        tr += '</span>';
        tr += '<input id="'+produto.id+'precoProdutoInput" type = "text" class = "form-control" name="precoProduto" value="'+produto.precoProduto+'"/>';

        tr += '</div>';

        tr += '<span id="'+produto.id+'precoProduto-span" class="help-block"> </span>';

        tr += '</div>';


        //Button Alterar

        tr += '<button id="AlterarProdutoButton'+produto.id+'" type="submit" class="btn btn-success btn-sm">';
        tr += '<span class="fa fa-exchange" aria-hidden="true"></span> Alterar';
        tr += '</button>';

        //Button Deletar

        tr += '<button id="btn-deletar-' + produto.id+'" type="submit" class="btn btn-danger btn-sm">';
        tr += '<span class="fa fa-trash" aria-hidden="true"></span> Deletar';
        tr += '</button>';
        tr += '<img src="/static/img/ajax.gif" id="alterandoProdutoFlag'+produto.id+'"/>';


        tr += '</div> </td> </tr>';


        $tbodyProdutos.append(tr);


        var $alterandoflag = $('#alterandoProdutoFlag'+produto.id);
        var $btnDeletar = $('#btn-deletar-' + produto.id);
        var $btnAlterar = $('#AlterarProdutoButton'+produto.id);

        var $nomeProdutoInputAlterar = $('#'+produto.id+'nomeProdutoInput');
        var $precoProdutoInputAlterar = $('#'+produto.id+'precoProdutoInput');



        $alterandoflag.hide();

        $btnDeletar.click(function () {
            $.post('/andris/categoria_produto/crudProduto/deletarProduto', {produto_id: produto.id}, function () {
                $("#tr-"+produto.id).remove();
            });
        });


        $btnAlterar.click(function(){

            function inputsProdutoAlterar() {


                return {
                    'produto_id': produto.id,
                    'nomeProduto': $nomeProdutoInputAlterar.val(),
                    'precoProduto': $precoProdutoInputAlterar.val()
                };

            }

            $.post('/andris/categoria_produto/crudProduto/editarProduto',inputsProdutoAlterar(),




                function(produto){
                    $alterandoFlag.hide();
                   $btnAlterar.show();
                    $btnDeletar.show();



                }).error(function(erro){

                    for (propriedade in erro.responseJSON){
                        $('#'+propriedade+'-div').addClass('has-error');
                        $('#'+propriedade+'-span').text(erro.responseJSON[propriedade]);

                    }


                }).always(function(){
                    $alterandoFlag.hide();
                    $btnAlterar.show();
                    $btnDeletar.show();


                });


        });


    }

    $.get('/andris/categoria_produto/crudProduto/listarProduto', function (produtos) {
        $.each(produtos, function (index, p) {
            adicionarProduto(p);
        });
    });



    var $adicionarButton = $('#AdicionarButton');
    $adicionarButton.click(



        function() {

            $('.has-error').removeClass('has-error');
            $('.help-block').empty();

            $salvandoProdutoFlag.fadeIn();

            $adicionarButton.attr('disabled', 'disabled');


            function obterInputsdeProduto() {


                return {
                    'categoria_id': $categoriaIdInput.val(),
                    'nomeProduto': $nomeProdutoInput.val(),
                    'precoProduto': $precoProdutoInput.val()
                };

            }


            $.post('/andris/categoria_produto/crudProduto/salvarProduto',obterInputsdeProduto(),


                function(produto){

                    adicionarProduto(produto);

                }).error(function(erro){

                    for (propriedade in erro.responseJSON){
                        $('#'+propriedade+'-div').addClass('has-error');
                        $('#'+propriedade+'-span').text(erro.responseJSON[propriedade]);

                    }


                }).always(function(){
                    $salvandoProdutoFlag.hide();
                    $adicionarButton.removeAttr('disabled');


                });


        } );

});
