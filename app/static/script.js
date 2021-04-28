$(document).ready(function(){
    $("select#search_cat").selectize({
        plugins: ["remove_button"],
        delimiter: ",",
        maxItems: 5,
        persist: false,
        create: function (input) {
        return {
            value: input,
            text: input,
        };
        },
    });
});