(function ($) {


    /**
     * Nomeia os dominios
     * Exemplo: Tipo = S/N --> Sim/Não
     * $('tag').NomeaEnum({
     *      S:"Sim", N:"Não"
     * });
     */
    $.fn.NomeaEnum = function (object) {
        $(this).each(function () {
            var key = $(this).text();
            $(this).text(object[key]);
        });
    }


}(jQuery));


