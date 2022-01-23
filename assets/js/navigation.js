let navExpanded = false;
const toggleNavMenu = () => {
    var navScroll = $('.nav-scroll');
    if(navExpanded){
        navScroll.removeClass('active');
        if($(window).width() > 447){
            $('.nav-watch').show();
        }
        $('#nav-icon3').removeClass('open');
        setTimeout(()=> {
            navScroll.addClass('hidden');
        }, 300);
        navExpanded = false;
    }
    else{
        navScroll.removeClass('hidden');
        $('.nav-watch').hide();
        setTimeout(()=> {
            navScroll.addClass('active');
            $('#nav-icon3').addClass('open');
        }, 50);
        navExpanded = true;
    }
}
$(document).on('click', '#nav-expand', () => {toggleNavMenu()});

