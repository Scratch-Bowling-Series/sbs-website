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
               $('.share-link').text(data.toString().replace('.pythonanywhere', ''));
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
       $('.share-link').css('color', 'red');
       navigator.clipboard.writeText(url);
       setTimeout(function (){
           $('.link-copy-notify').css('opacity', 0);
       },2000);
   }
});