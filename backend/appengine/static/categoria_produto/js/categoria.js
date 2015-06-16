var categoriaModulo = angular.module('categoriaModulo',['rest']);

categoriaModulo.directive('categoriaform',function(){

    return{
        restrict:'E',
        replace:true,
        templateUrl:'/static/categoria_produto/html/categoria_form.html',
        scope:{
            categoria:'=',
            nomeLabel:'@',
            saveComplete:'&'

        },
        controller:function($scope,CategoriaApi){
            $scope.salvandoFlag = false;
            $scope.salvarCategoria = function(){

                $scope.salvandoFlag = true;
                $scope.errors = {};



                CategoriaApi.salvarCategoria($scope.categoria).success(function(categoria) {

                    $scope.categoria.nomeCategoria = '';

                    if ($scope.saveComplete != undefined) {

                        $scope.saveComplete({'categoria':categoria});
                    }

                    $scope.salvandoFlag = false;


                }).error(function(erros){

                    $scope.errors = erros;
                    $scope.salvandoFlag = false;

                })


            }

        }


    };

});





categoriaModulo.directive('categorialinha',function(){

    return{
        replace:true,
        templateUrl:'/static/categoria_produto/html/categoria_linha_tabela.html',
        scope:{
            categoria:'=',
            deleteComplete:'&',
            editComplete:'&'


        },
        controller:function($scope,CategoriaApi){
            $scope.ajaxFlag = false;
            $scope.editingFlag = false;
            $scope.categoriaEditar = {}

            $scope.categoriaEditar.id = $scope.categoria.id;
            $scope.categoriaEditar.nomeCategoria = $scope.categoria.nomeCategoria;


            $scope.deletarCategoria = function(){
                $scope.ajaxFlag = true;
                CategoriaApi.deletarCategoria($scope.categoria.id).success(function(){
                    $scope.deleteComplete({'categoria':$scope.categoria});

                }).error(function(){



                });
            }

            $scope.editarCategoria = function(){
                $scope.editingFlag = true;




                $scope.errors = {};
                CategoriaApi.editarCategoria($scope.categoriaEditar).success(function(categoria){

                    $scope.categoria = categoria;


                    $scope.editingFlag = false;
                }).error(function(erros){

                    $scope.errors = erros;
                    $scope.editingFlag = false;

                })




            }



        }


    };

});



$(document).ready(function(){

    var $btnJumbo = $('#btnUploadJumbotron');
    var $imgJumbo = $('#imgJumbo');
    var $inpUpload = $('#uploadInput');



    //$imgJumbo.attr('src','../static/img/fotonaodisponivel.jpg');

    var reader = new FileReader();

    $inpUpload.change(function () {
        readURL(this);
    });

    function readURL(input) {
        if (input.files && input.files[0]) {

            reader.onload = function (e) {
                $imgJumbo.attr('src', e.target.result);
            }

            reader.readAsDataURL(input.files[0]);
        }
    }


    $.get('/andris/updown/dowload', function (arquivo) {
        $.each(arquivo, function (index, p) {
            adicionarProduto(p);
        });
    });




});







