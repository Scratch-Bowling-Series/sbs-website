$(document).ready(function() {
    var height_diff = $(window).height() - ($('footer').offset().top + $('footer').height() - 20);
    if (height_diff > 0) {
        console.log(height_diff)
        $('footer').css('margin-top', height_diff);
    }
    $('footer').css('opacity', '1');

    var closed = true;
    $('#nav-expand').click(function(){
        if(closed)
        {
            closed = false;
            $('.nav-scroll').show();
            setTimeout(function ()
            {
                $('.nav-scroll').css('height', '230px');
                $('.nav-scroll').css('border-color', '#214031');
                $('.nav-scroll').css('box-shadow', '0 10px 5px rgba(0,0,0,0.2)');
                $('#nav-icon3').addClass('open');
            }, 50);
        }
        else
        {
            closed = true;
            $('.nav-scroll').css('height', '0px');
            $('.nav-scroll').css('border-color', 'white');
            $('.nav-scroll').css('box-shadow', '0 20px 5px transparent');
            setTimeout(function()
            {
                $('.nav-scroll').hide();
            }, 300);
            $('#nav-icon3').removeClass('open');
        }
    });



});