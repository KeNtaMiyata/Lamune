function long_text(text){
    var slicetext = text.length > 30 ? (text).slice(0,20)+"…" : text;
    document.write(slicetext);
}

jquery(function($){

    $("tr[data-href").addClass("clickable").on("click", function(e){
        if (!$(e.target).is('a')) {
            window.location = $(e.target).closest.data('href');
        }
    });
});

