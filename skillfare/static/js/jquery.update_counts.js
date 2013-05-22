// $.getScript("jquery.getcsrftoken.js", function(){
//    alert("Script loaded and executed.");
//    // here you can use anything you defined in the loaded script
// });


function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    crossDomain: false, // obviates need for sameOrigin test
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type)) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function update_count() {
    var count = $(this).next("span.interest_count");
    var id = $(this).parent().find("a.more").attr("href").match(/\/sharedbookmark\/detail\/([0-9]+)/)[1];
    var url = "/bookmark/interested/" + id + "/";
    $.post(url, function (result) {
        count.text(result);
    });
    return false;
};

$(document).ready(function () {
    $("ul.bookmarks .interested").click(update_count);
});



