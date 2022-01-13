let navExpanded = false;
const toggleNavMenu = () => {
    var navScroll = $('.nav-scroll');
    if(navExpanded){
        navScroll.css('max-height', '0px');
        navScroll.css('border-color', 'white');
        navScroll.css('box-shadow', '0 20px 5px transparent');
        setTimeout(function() {
            $('.nav-scroll').hide();
        }, 300);
        $('#nav-icon3').removeClass('open');
        navExpanded = false;
    }
    else{
        navScroll.show();
        setTimeout(function () {
            navScroll.css('max-height', '2000px');
            navScroll.css('border-color', '#214031');
            navScroll.css('box-shadow', '0 10px 5px rgba(0,0,0,0.2)');
            $('#nav-icon3').addClass('open');
        }, 50);
        navExpanded = true;
    }
}
$(document).on('click', '#nav-expand', ()=> toggleNavMenu());

