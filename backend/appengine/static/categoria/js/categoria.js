var categoriaModulo = angular.module('categoriaModulo',['rest']);

categoriaModulo.directive('categoriaform',function(){

    return{
        restrict:'E',
        replace:true,
        templateUrl:'/static/categoria/html/categoria_form.html',
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
        templateUrl:'/static/categoria/html/categoria_linha_tabela.html',
        scope:{
            categoria:'=',
            deleteComplete:'&'

        },
        controller:function($scope,CategoriaApi){
            $scope.ajaxFlag = false;
            $scope.deletarCategoria = function(){
                $scope.ajaxFlag = true;
                CategoriaApi.deletarCategoria($scope.categoria.id).success(function(){
                    $scope.deleteComplete({'categoria':$scope.categoria});

                }).error(function(){



                });
            }



        }


    };

});