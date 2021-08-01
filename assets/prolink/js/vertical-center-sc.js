$(document).ready(function()
        {
            Align();
            $(window).resize(function()
            {
                Align();
            });
            $('.sc').change(function()
            {
                console.log('changed');
                Align();
            });
            function Align()
            {
                var element = $('.center-vertically');
                var windowHeight = $(window).height() - 25;
                var height = element.height();
                var margin = ((windowHeight - height) / 2);
                if(margin < 10){ margin = 10;}
                element.css('margin-top', margin);
            }
        });