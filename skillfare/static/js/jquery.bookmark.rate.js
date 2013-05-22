$(document).ready(function() {
     $('.thingrating').each(function(index){
      $(this).raty({
        readOnly:  false,
        width: 110,
        path: "/static/images/",
        score: $(this).children("span:first").text(),
        click: function(score, evt) {
            var vote_url = "/bookmark/rate/" + $(this).attr('id') + "/" + score + "/";
            $.ajax({
              url: vote_url,
              success: function(){
                alert('vote successful');
              }, 
              error: function(jqXHR, textStatus, errorThrown){
                alert("\ntextStatus: " + textStatus + "\nerrorThrown: " + errorThrown)
              }
            });
        }
      });
    });
});