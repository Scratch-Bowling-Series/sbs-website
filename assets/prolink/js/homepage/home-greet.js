$(document).ready(function() {


    Greet();
    function Greet()
    {
        if(sessionStorage.hasGreeted != 'yes')
        {
            var format="";
            var ndate = new Date();
            var hr = ndate.getHours();
            var h = hr % 12;

             if (hr < 12)
             {
                greet = 'Good Morning';
                format='AM';
                }
            else if (hr >= 12 && hr <= 17)
            {
                greet = 'Good Afternoon';
                format='PM';
                }
            else if (hr >= 17 && hr <= 24)
                greet = 'Good Evening';

            if (h < 12) {
              h = "0" + h;
              $("#homepage-wrap span.greeting").html(greet);
            } else if (h < 18) {
              $("#homepage-wrap span.greeting").html(greet);
            } else {
              $("#homepage-wrap span.greeting").html(greet);
            }
            Transition();
            sessionStorage.hasGreeted = 'yes';
        }
        else
        {
            $('#homepage-wrap h2').css('display','none');
            $('#homepage-wrap').css('display','none');
            $('#homepage-content').css('display','block');
            $('#homepage-content').css('opacity','1');
        }
    }

    function Transition() {
        $('#homepage-wrap h2').css('transition','opacity 0s');
        $('#homepage-wrap h2').css('opacity','1');
        $('#homepage-wrap h2').css('transition','opacity 1s');
        setTimeout(function()
        {
            $('#homepage-wrap h2').css('opacity','0');
            setTimeout(function()
            {
                $('#homepage-wrap h2').css('display','none');
                $('#homepage-wrap').css('display','none');
                $('#homepage-content').css('display','block');
                $('#homepage-content').css('opacity','1');
            }, 1000);
        }, 1000);
    }
});