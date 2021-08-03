$(document).ready(function()
      {
        var offline = true;
        var ping = require('ping');
        var host = '127.0.0.1';

        PingServer(host);

        const interval = setInterval(function()
        {
          PingServer(host);
        }, 4000);


        function PingServer(url)
        {
          ping.promise.probe(host,
          {
            timeout: 5,
          }).then(function (res) {
            if(res.time != 'unknown')
            {
                Online(res.time);
            }
            else
            {
              Offline();
            }
          });
        }

        function Offline()
        {
            setTimeout(function()
            {
              offline = true;
                $('#con-ping').html('OFFLINE');
                $('#con-ping-icon').css('color','red');
                $('#con-ping-icon').removeClass('fa-circle');
                $('#con-ping-icon').addClass('fa-sync-alt');
                $('#con-ping-icon').css('font-size', '10px');
                $('#con-ping-icon').css('padding', '2px 2px 2px 2px');
                $('#con-ping-icon').css('transition', 'transform linear 2s');
                $('#con-ping-icon').css('transform', 'rotate(10000deg)');
              setTimeout(function()
              {
                $('#con-ping-icon').removeClass('fa-sync-alt');
                $('#con-ping-icon').addClass('fa-circle');
                $('#con-ping-icon').css('color','red');
                $('#con-ping-icon').css('transition', 'none');
                $('#con-ping-icon').css('font-size', '6px');
                $('#con-ping-icon').css('padding', '3px 1px 1px 1px');
                $('#con-ping-icon').removeClass('fa-sync-alt');
                $('#con-ping-icon').addClass('fa-circle');
              }, 1000);
            }, 400);
        }
        function Online(ping)
        {
            setTimeout(function()
            {
              offline = false;
              $('#con-ping').html(ping + 'ms');
              $('#con-ping-icon').css('transition', 'none');
              $('#con-ping-icon').css('font-size', '6px');
              $('#con-ping-icon').css('padding-top', '3px');
              $('#con-ping-icon').removeClass('fa-sync-alt');
              $('#con-ping-icon').addClass('fa-circle');

              if(ping <= 20)
              {
                $('#con-ping-icon').css('color','#9d9fa1');
              }
              else if(ping <= 60)
              {
                $('#con-ping-icon').css('color','orange');
              }
              else
              {
                $('#con-ping-icon').css('color','red');
              }
            }, 1000);
        }
      });