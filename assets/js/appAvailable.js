
$(document).ready(() => {
    var is_opera = !!window.opera || navigator.userAgent.indexOf(' OPR/') >= 0;
    var is_Edge = navigator.userAgent.indexOf("Edge") > -1;
    var is_chrome = !!window.chrome && !is_opera && !is_Edge;
    var is_explorer= typeof document !== 'undefined' && !!document.documentMode && !is_Edge;
    var is_safari = /^((?!chrome|android).)*safari/i.test(navigator.userAgent);
    var is_duckduck = navigator.userAgent.indexOf("DuckDuckGo") > -1;

    var opera_icon = '/static/img/opera_icon.png';
    var edge_icon = '/static/img/edge_icon.png';
    var chrome_icon = '/static/img/chrome_icon.png';
    var explore_icon = '/static/img/explore_icon.png';
    var firefox_icon = '/static/img/firefox_icon.png';
    var safari_icon = '/static/img/safari_icon.png';
    var duckduck_icon = '/static/img/duckduck_icon.png';
    var default_icon = '/static/img/default_web_icon.png';

    if(is_opera){
        $('.bottom-up .browser-icon').attr('src', opera_icon);
    }else if(is_Edge){
        $('.bottom-up .browser-icon').attr('src', edge_icon);
    }else if(is_chrome){
        $('.bottom-up .browser-icon').attr('src', chrome_icon);
    }else if(is_explorer){
        $('.bottom-up .browser-icon').attr('src', explore_icon);
    }else if(is_duckduck){
        $('.bottom-up .browser-icon').attr('src', duckduck_icon);
    }else if(is_safari){
        $('.bottom-up .browser-icon').attr('src', safari_icon);
    }else {
        $('.bottom-up .browser-icon').attr('src', default_icon);
    }

    var android = (/android/i.test(navigator.userAgent));

    if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        if(sessionStorage.getItem('appAvailable') !== 'shown' && $(window).width() < 992){
            $('.bottom-up').addClass('visible');
            $('body').addClass('no-scroll');
        }
    }

    $('.open-sbs-bowler').click(()=>{
        setTimeout(()=>{
            if(android){
                window.location = 'https://play.google.com'
            }else{
                window.location = 'https://www.apple.com/app-store/'
            }
        }, 500);
        window.location = 'sbs-bowler://home'
    });

    $('.open-sbs-mobile').click(()=>{
        setTimeout(()=>{
            if(android){
                window.location = 'https://play.google.com'
            }else{
                window.location = 'https://www.apple.com/app-store/'
            }
        }, 500);
        window.location = 'sbs-mobile://home'
    });

    $('.bottom-up .continue').click(()=>{
        $('.bottom-up').removeClass('visible');
        $('body').removeClass('no-scroll');
        sessionStorage.setItem('appAvailable', 'shown');
    });
});