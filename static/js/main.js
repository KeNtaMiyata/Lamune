function long_text(text){
    var slicetext = text.length > 20 ? (text).slice(0,20)+"…" : text;
    document.write(slicetext);
}