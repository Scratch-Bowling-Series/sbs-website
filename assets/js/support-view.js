$(document).ready(function() {
    updateDonorBar(getRandomArbitrary(8000, 90000));

    function getRandomArbitrary(min, max) {
      return Math.random() * (max - min) + min;
    }

    function updateDonorBar(amount)
    {
    $('.support-goals-slide-bar-inner').css('bottom','auto');
    var height = $('.support-goals-slide-bar').height();
    var maxheight = height * 7;
    if(amount > 0)
    {
        var mult = amount / 15000;
        $('.goal-1').css('height', height * mult + 'px');
        $('.goal-1').css('max-height', height + 'px');
        $('.goal-1').css('min-height', 20 + 'px');
        $('.goal-1-dot').removeClass('off');

    }
    else
    {
        $('.goal-1-dot').addClass('off');
    }
    if(amount >= 15000)
    {
        amount = amount - 15000;
        var mult = amount / 15000;
        $('.goal-2').css('height', height * mult + 'px');
        $('.goal-2').css('max-height', height + 'px');
        $('.goal-2').css('min-height', 20 + 'px');
        $('.goal-2-dot').removeClass('off');

    }
    else
    {
        $('.goal-2-dot').addClass('off');
    }
    if(amount >= 15000)
    {
        amount = amount - 15000;
        var mult = amount / 15000;
        $('.goal-3').css('height', height * mult + 'px');
        $('.goal-3').css('max-height', height + 'px');
        $('.goal-3').css('min-height', 20 + 'px');
        $('.goal-3-dot').removeClass('off');
    }
    else
    {
        $('.goal-3-dot').addClass('off');

    }
    if(amount >= 15000)
    {
        amount = amount - 15000;
        var mult = amount / 40000;
        $('.goal-4').css('height', height * mult + 'px');
        $('.goal-4').css('max-height', height + 'px');
        $('.goal-4').css('min-height', 20 + 'px');
        $('.goal-4-dot').removeClass('off');

    }
    else
    {
        $('.goal-4-dot').addClass('off');
    }
    if(amount >= 40000)
    {
        amount = amount - 40000;
        var mult = amount / 35000;
        $('.goal-5').css('height', height * mult + 'px');
        $('.goal-5').css('max-height', height + 'px');
        $('.goal-5').css('min-height', 20 + 'px');
        $('.goal-5-dot').removeClass('off');
    }
    else
    {
        $('.goal-5-dot').addClass('off');
    }
    if(amount >= 35000)
    {
        amount = amount - 35000;
        var mult = amount / 80000;
        $('.goal-6').css('height', height * mult + 'px');
        $('.goal-6').css('max-height', height + 'px');
        $('.goal-6').css('min-height', 20 + 'px');
        $('.goal-6-dot').removeClass('off');
    }
    else
    {
        $('.goal-6-dot').addClass('off');
    }
    if(amount >= 80000)
    {
        $('.goal-7').css('height', '10px');
        $('.goal-7').css('max-height', height + 'px');
        $('.goal-7').css('min-height', 20 + 'px');
        $('.goal-7-dot').removeClass('off');
    }
    else
    {
        $('.goal-7-dot').addClass('off');
    }
    }
});