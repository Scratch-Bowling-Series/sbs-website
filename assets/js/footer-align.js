var navExpanded = false;

$(document).ready(function() {
    toggleNavMenu();

    updateFooterMargins();
    $(window).change(function(){
        updateFooterMargins();
    });
    $(document).on('click', '#nav-expand', function(){
        toggleNavMenu()
    });
});

function toggleNavMenu(){
    var navScroll = $('.nav-scroll');
    if(navExpanded){
        navScroll.css('max-height', '0px');
        navScroll.css('border-color', 'white');
        navScroll.css('box-shadow', '0 20px 5px transparent');
        setTimeout(function()
        {
            $('.nav-scroll').hide();
        }, 300);
        $('#nav-icon3').removeClass('open');
        navExpanded = false;
    }
    else{
        navScroll.show();
        setTimeout(function ()
        {
            navScroll.css('max-height', '2000px');
            navScroll.css('border-color', '#214031');
            navScroll.css('box-shadow', '0 10px 5px rgba(0,0,0,0.2)');
            $('#nav-icon3').addClass('open');
        }, 50);
        navExpanded = true;
    }
}

function updateFooterMargins(){
    var footer = $('footer');
    var height_diff = $(window).height() - (footer.offset().top + footer.height());
    if (height_diff > 0) {
        footer.css('margin-top', height_diff + 10);
    }
    else{
        footer.css('margin-top', 10);
    }
    footer.css('opacity', '1');
}