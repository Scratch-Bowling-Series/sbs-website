$(document).ready(function()
{
    var registered_autfields = [];
    var opened_autofield = null;
    function AutoFieldRegistered(element) {
        var found = false;
        if(registered_autfields != null)
        {
            for(var i = 0; i < registered_autfields.length; i++) {
                if (registered_autfields[i] == element) {
                    found = true;
                    break;
                }
            }
            if(!found)
            {
                registered_autfields.push(element);
                return true;
            }
        }
        else
        {
            registered_autfields = new Array(element);
        }

        return false;
    }


    $('html').click(function(e) {
        if(opened_autofield != null)
        {
            opened_autofield.next().find('div').css('max-height', 0);
            opened_autofield.parent().css('z-index',1);
            opened_autofield = null;
        }
    });

    $('.scroll-wrap').on('click', '.autofield-selector', function()
    {
        var form = $(this).parent().parent().parent().find('.autofield-input');
        var name = $(this).find('span').text();
        var id = $(this).attr('data');
        form.val(name);
        form.next().find('div').css('max-height', 0);
        form.parent().css('z-index',1);
        opened_autofield = null;
    });

    $('.autofield-input').keyup(function()
    {
        if(AutoFieldRegistered(this)) {
            console.log("New Autofield Registered.")
        }
        var form = $(this);
        var scrollWrap = form.next().find('div');
        var fieldType = form.attr('data');
        var text = form.val();
        scrollWrap.css('max-height', 500);
        opened_autofield = form;
        form.parent().css('z-index', 500);
        var queryUrl = '/prolink/' + fieldType+ '/autofield/' + text + '/'
        $.getJSON(queryUrl, function(data) {
            scrollWrap.empty();
            $.each(data, function(index, pattern)
            {
                Add(pattern, scrollWrap);
            });
        });
    });

    function Add(result, element)
    {
        generated_html = '<a class="autofield-selector" data="' + result[1] +'"><span>';
        generated_html += result[0];
        generated_html += '</span><i>';
        generated_html += result[1];
        generated_html += '</i></a>';
        element.append(generated_html);
    }
});