$(document).ready(function(){
   $('.sharebox .close').click(function (){
       $('.sharebox').hide();
   });
   $('.share-page').click(function(){
        console.log('sharing');
      var pageUrl = window.location.href;
       $.ajax({
           type: "POST",
           url: "https://scratchbowling.pythonanywhere.com/s/create/new/",
           data: { url: pageUrl }
           contentType: "text/plain",
           dataType: "text",
           success: function (data) {
                        $('.sharebox').show();
                        $('.share-link').text(data.toString());
                        $('.share-link').click(function (){ CopyTo(data.toString()); });
                        $('.link-copy').click(function (){ CopyTo(data.toString()); });
           }
       });
   });

   function CopyTo(url){
       $('.link-copy-notify').show();
       setTimeout(function (){
           $('.link-copy-notify').hide();
       },2000);
       navigator.clipboard.writeText(url);
   }
});