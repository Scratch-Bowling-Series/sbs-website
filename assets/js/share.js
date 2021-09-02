$(document).ready(function(){
   $('.sharebox .close').click(function (){
       $('.sharebox').hide();
   });
   $('.share-page').click(function(){
      var pageUrl = window.location.href;
      pageUrl = pageUrl.replace('https://scratchbowling.pythonanywhere.com', '');
      pageUrl = pageUrl.replaceAll('/', '&sl');
       $.ajax({
           type: "GET",
           url: "https://scratchbowling.pythonanywhere.com/s/create/new/" + pageUrl,
           contentType: "text/plain",
           dataType: "text",
           success: function (data) {
               OpenShareBox();
               $('.share-link').html(data.toString().replace('.pythonanywhere', '') + '<span id="link-notify" class="link-copy-notify">LINK COPIED TO CLIPBOARD</span>');
               $('.share-link').click(function (){ CopyTo(data.toString()); });
               $('.link-copy').click(function (){ CopyTo(data.toString()); });
           }
       });
   });

   $('.share-page-direct').click(function(){
      var pageUrl = $('.share-page-direct').attr('data');
      pageUrl = pageUrl.replace('https://scratchbowling.pythonanywhere.com', '');
      pageUrl = pageUrl.replaceAll('/', '&sl');
       $.ajax({
           type: "GET",
           url: "https://scratchbowling.pythonanywhere.com/s/create/new/" + pageUrl,
           contentType: "text/plain",
           dataType: "text",
           success: function (data) {
               OpenShareBox();
               $('.share-link').html(data.toString().replace('.pythonanywhere', '') + '<span id="link-notify" class="link-copy-notify">LINK COPIED TO CLIPBOARD</span>');
               $('.share-link-facebook').attr('data-href', data.toString());
               $('.share-link').click(function (){ CopyTo(data.toString()); });
               $('.link-copy').click(function (){ CopyTo(data.toString()); });
           }
       });
   });

   function OpenShareBox(){
        $('.sharebox').css('display', 'block');
        $('.link-copy-notify').css('opacity', 0);

   }

   function CopyTo(url){
       $('.link-copy-notify').css('opacity', 1);
       navigator.clipboard.writeText(url);
       setTimeout(function (){
           $('.link-copy-notify').css('opacity', 0);
       },1000);
   }
});