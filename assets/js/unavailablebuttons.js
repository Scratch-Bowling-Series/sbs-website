$(document).ready(function(){
    var untext = 'W.I.P.'

    $('.unavailable-btn').click(function(){
        if($(this).text() != untext){
            var btn = $(this);
            var width = $(this).outerWidth();
            console.log(width);
            $(this).css('width', width);
            var temp = $(this).text();
            $(this).html(untext);
            setTimeout(function(){
                btn.html(temp);
            }, 2000);
        }
    });
});