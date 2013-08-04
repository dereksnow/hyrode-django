$(document).ready(function() {
     $('.thingrating').each(function(index){
      $(this).raty({
        readOnly:  false,
        width: 110,
        path: "/static/images/",
        score: $(this).children("span:first").text(),
        click: function(score, evt) {
            var vote_url = "/bookmark/rate/" + $(this).attr('id') + "/" + score + "/";
            $.post(vote_url, function(){
                alert('vote successful');
              }).fail(function(jqXHR, textStatus, errorThrown){
                  alert("\ntextStatus: " + textStatus + "\nerrorThrown: " + errorThrown);});
        }
      });
    });

     $('.pathrating').each(function(index){
      $(this).raty({
        readOnly:  false,
        width: 110,
        path: "/static/images/",
        score: $(this).children("span:first").text(),
        click: function(score, evt) {
            var vote_url = "/path/rate/" + $(this).attr('id') + "/" + score + "/";
            $.post(vote_url, function(){
                alert('vote successful');
              }).fail(function(jqXHR, textStatus, errorThrown){
                  alert("\ntextStatus: " + textStatus + "\nerrorThrown: " + errorThrown);});
        }
      });
    });

});



