$(document).ready(function() {
    var height_diff = $(window).height() - ($('footer').offset().top + 50);
    if (height_diff > 0) {
        console.log(height_diff)
        $('footer').css('margin-top', height_diff);
    }

    var closed = true;
    $('#nav-drop-button').click(function(){
        if(closed)
        {
            closed = false;
            $('#nav-account').css('display', 'flex');
            $('.nav-buttons').css('display', 'block');
            $('#nav-drop-button i').css('text-shadow', '-1px -1px 0 #d9af62,  1px -1px 0 #d9af62,-1px 1px 0 #d9af62,1px 1px 0 #d9af62');
        }
        else
        {
            closed = true;
            $('#nav-account').css('display', 'none');
            $('.nav-buttons').css('display', 'none');

            $('#nav-drop-button i').css('text-shadow', 'none');
        }
    });

});