function long_text(text){
    var slicetext = text.length > 30 ? (text).slice(0,20)+"…" : text;
    document.write(slicetext);
}

function confirm_delete(){
    if (confirm( "この問題を削除してよいですか？" )){
        return true;
    }
    else{
        return false
    }
}

function show_datetime(datetime){
    // 2022-08-10 04:00:48.899189 必要なのは19文字
    var show = (datetime).slice(0,19);
    document.write(show);
}

// jquery(function($){

//     $("tr[data-href").addClass("clickable").on("click", function(e){
//         if (!$(e.target).is('a')) {
//             window.location = $(e.target).closest.data('href');
//         }
//     });
// });


