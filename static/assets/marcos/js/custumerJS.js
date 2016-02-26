function checkAllSN(){
    var checkSN = document.getElementsByClassName('checkbox-sn');
    for(var i = 0; i < checkSN.length; i++){
        if(checkSN[i].value=='S'){
            checkSN[i].checked = true;
        }else{
            checkSN[i].checked = false;
        }
        checkSN[i].addEventListener("click",onclickCheckSN);
    }
}

function onclickCheckSN(e){
    if(this.checked){
        this.value = 'S';
    }else{
        this.value = 'N';
    }
}

function getPTbr_DataTable(){
    return (
            {
                "sEmptyTable": "Nenhum registro encontrado",
                "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
                "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
                "sInfoFiltered": "(Filtrados de _MAX_ registros)",
                "sInfoPostFix": "",
                "sInfoThousands": ".",
                "sLengthMenu": "_MENU_ resultados por página",
                "sLoadingRecords": "Carregando...",
                "sProcessing": "Processando...",
                "sZeroRecords": "Nenhum registro encontrado",
                "sSearch": "Pesquisar",
                "oPaginate": {
                    "sNext": "Próximo",
                    "sPrevious": "Anterior",
                    "sFirst": "Primeiro",
                    "sLast": "Último"
                },
                "oAria": {
                    "sSortAscending": ": Ordenar colunas de forma ascendente",
                    "sSortDescending": ": Ordenar colunas de forma descendente"
                }
            }
    );
}

