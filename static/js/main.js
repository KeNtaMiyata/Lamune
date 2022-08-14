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

