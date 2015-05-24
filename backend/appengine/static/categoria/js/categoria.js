var categoriaModulo = angular.module('categoriaModulo',['rest']);

categoriaModulo.directive('categoriaform',function(){

    return{
        restrict:'E',
        replace:true,
        templateUrl:'/static/categoria/html/categoria_form.html',
        scope:{
            categoria:'=',
            nomeLabel:'@'
        },
        controller:function($scope,CategoriaApi){
            $scope.salvandoFlag = false;
            $scope.salvarCategoria = function(){

                $scope.salvandoFlag = true;
                $scope.errors = {};



                CategoriaApi.salvarCategoria($scope.categoria).success(function(categoria){


                    $scope.categoria.nomeCategoria = '';
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
        restrict:'A',
        replace:true,
        templateUrl:'/static/categoria/html/categoria_linha_tabela.html',
        scope:{
            categoria:'='

        },
        controller:function($scope,CategoriaApi){





        }


    };

});