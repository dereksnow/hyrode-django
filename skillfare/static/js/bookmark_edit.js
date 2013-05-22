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

function bookmark_edit() {
    var item = $(this).parent();
    var url = item.find(".title").attr("href");
    item.load(
        "/bookmark/save/?url=" + encodeURIComponent(url),
        null,
        function() {
            $("#save-form").submit(bookmark_save);
        }
    );
    return false;
};

$(document).ready(function () {
    $("ul.bookmarks .edit").click(bookmark_edit);
});

function bookmark_save() {
    var item = $(this).parent();
    var features_list = [];
    for(var i = 0; i < 4; i++)
    {
        var cur_feature = "#id_features_" + i; 
        if($(cur_feature).is(":checked"))
        {
            features_list.push($(cur_feature).val());
        }
    }
    features_list = feature_list.join();
    var data = {
        title: item.find("#id_title").val(),
        personal: item.find("#id_personal").val(),
        tags: item.find("#id_tags").val(),
        features: features_list
    };
    $.post("/bookmark/save/", data, function (result) {
        if (result != "failure") {
            alert(result);
            //alert($("ul.bookmarks li:first"));
            //item.after($("ul.bookmarks li:first"));
            item.after($("li", $.parseHTML(result)).get(0));
            item.remove();
            $("ul.bookmarks .edit").click(bookmark_edit);
        }
        else{
            alert("Failed to validate bookmark before saving.");
        }
    });
    return false;
};