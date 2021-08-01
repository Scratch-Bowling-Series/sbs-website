$(document).ready(function()
      {
        var offline = true;
        var ping = require('ping');
        var host = '107.0.0.1';

        Offline();
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
          offline = true;
            $('#con-ping').html('OFFLINE');
            $('#con-ping-icon').css('color','red');
            $('#con-ping-icon').removeClass('fa-circle');
            $('#con-ping-icon').addClass('fa-sync-alt');
            $('#con-ping-icon').css('font-size', '10px');
            $('#con-ping-icon').css('padding', '2px 2px 2px 2px');
            $('#con-ping-icon').css('transition', 'transform linear 25s');
            $('#con-ping-icon').css('transform', 'rotate(10000deg)');
          setTimeout(function()
          {
            $('#con-ping-icon').removeClass('fa-sync-alt');
            $('#con-ping-icon').addClass('fa-circle');
            $('#con-ping-icon').css('color','red');
            $('#con-ping-icon').css('transition', 'none');
            $('#con-ping-icon').css('font-size', '6px');
            $('#con-ping-icon').css('padding', '5px 2px 0 0');
            $('#con-ping-icon').removeClass('fa-sync-alt');
            $('#con-ping-icon').addClass('fa-circle');
          }, 1000);
        }
        function Online(ping)
        {
          offline = false;
          $('#con-ping').html(ping + 'ms');
          $('#con-ping-icon').css('transition', 'none');
          $('#con-ping-icon').css('font-size', '6px');
          $('#con-ping-icon').css('padding-top', '4px');
          $('#con-ping-icon').removeClass('fa-sync-alt');
          $('#con-ping-icon').addClass('fa-circle');

          if(ping <= 20)
          {
            $('#con-ping-icon').css('color','white');
          }
          else if(ping <= 60)
          {
            $('#con-ping-icon').css('color','orange');
          }
          else
          {
            $('#con-ping-icon').css('color','red');
          }
        }
      });