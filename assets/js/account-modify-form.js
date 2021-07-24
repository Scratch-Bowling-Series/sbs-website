$( document ).ready(function() {
    $("input[type='checkbox']").change(function(){
        UpdateDexterityText()
      });
    UpdateDexterityText();

    function UpdateDexterityText(checkbox)
    {
        if(checkbox)
        {
        }
        else
        {

        }

        var text = "";
        var handright = $(".standard-form-dexterity-right input").is(":checked");
        var handleft = $(".standard-form-dexterity-left input").is(":checked");
        if(handright){
          $(".standard-form-dexterity-right input").prev().removeClass("hand-off");
        }else{
          $(".standard-form-dexterity-right input").prev().addClass("hand-off");
        }
        if(handleft){
          $(".standard-form-dexterity-left input").prev().removeClass("hand-off");
        }else{
          $(".standard-form-dexterity-left input").prev().addClass("hand-off");
        }

        if(handleft && handright)
        {
            text = "TWO HANDED";
        }
        else if(handleft && handright == false)
        {
            text = "LEFT HANDED";
        }
        else if(handleft == false && handright)
        {
            text = "RIGHT HANDED";
        }
        else
        {
            text = "";
        }
        $(".standard-form-dexterity-text").html(text);
    }



});