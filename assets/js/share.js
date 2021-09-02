$(document).ready(function(){
   $('.sharebox .close').click(function (){
       $('.sharebox').hide();
   });
   $('.share-page').click(function(){
      //$('#link-notify').css('opacity', 0);
      var pageUrl = window.location.href;
      pageUrl = pageUrl.replace('https://scratchbowling.pythonanywhere.com', '');
      pageUrl = pageUrl.replaceAll('/', '&sl');
       $.ajax({
           type: "GET",
           url: "https://scratchbowling.pythonanywhere.com/s/create/new/" + pageUrl,
           contentType: "text/plain",
           dataType: "text",
           success: function (data) {
                        $('.sharebox').css('display', 'block');
                        $('.link-copy-notify').css('opacity', '0');
                        $('.share-link').text(data.toString().replace('.pythonanywhere', ''));
                        $('.share-link').click(function (){ CopyTo(data.toString()); });
                        $('.link-copy').click(function (){ CopyTo(data.toString()); });
           }
       });
   });

   function CopyTo(url){
       $('#link-notify').css('opacity', 1);
       console.log('opacity 1' + $('#link-notify').css('opacity'));
       navigator.clipboard.writeText(url);
       setTimeout(function (){
           $('#link-notify').css('opacity', 0);
       },2000);
   }
});