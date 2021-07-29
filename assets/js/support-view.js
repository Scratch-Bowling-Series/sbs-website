$(document).ready(function() {
    updateDonorBar({{ donation_count }});

    function updateDonorBar(amount)
    {
        var height = 120;
        var maxheight = height * 7;
        if(amount > 120000)
        {
            var mult = amount / 80000;
            $('.goal-7').css('height', height * mult + 'px');
            $('.goal-7-dot').addClass('off');
            HideSpecific('.prev-goal-7');
        }
        else if(amount > 85000)
        {
            var mult = amount / 35000;
            $('.goal-6').css('height', height * mult + 'px');
            $('.goal-6-dot').addClass('off');
            HideSpecific('.prev-goal-6');
        }
        else if(amount > 45000)
        {
            var mult = amount / 40000;
            $('.goal-5').css('height', height * mult + 'px');
            $('.goal-5-dot').addClass('off');
            HideSpecific('.prev-goal-5');
        }
        else if(amount > 30000)
        {
            var mult = amount / 15000;
            $('.goal-4').css('height', height * mult + 'px');
            $('.goal-4-dot').addClass('off');
            HideSpecific('.prev-goal-4');
        }
        else if(amount > 15000)
        {
            var mult = amount / 15000;
            $('.goal-3').css('height', height * mult + 'px');
            $('.goal-3-dot').addClass('off');
            HideSpecific('.prev-goal-3');
        }
        else if(amount > 0)
        {
            var mult = amount / 15000;
            $('.goal-2').css('height', height * mult + 'px');
            $('.goal-2-dot').addClass('off');
            HideSpecific('.prev-goal-2');
        }
    }
    function HideSpecific(goal)
    {
        $('.prev-goal-1').css('display','none');
        $('.prev-goal-2').css('display','none');
        $('.prev-goal-3').css('display','none');
        $('.prev-goal-4').css('display','none');
        $('.prev-goal-5').css('display','none');
        $('.prev-goal-6').css('display','none');
        $('.prev-goal-7').css('display','none');
        $(goal).css('display','block')
    }
});