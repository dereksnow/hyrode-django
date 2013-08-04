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

function update_like_count() {
    var count = $(this).parents("article").find("span.interest_count");

    var type = $("span.resource-type").text();
    var id = $(this).closest("div").find("a.more").attr("href").match(/\/sharedbookmark\/detail\/([0-9]+)/)[1];    
    if (type === "path")
    {
        var url = "/path/interested/" + id + "/";
    }
    else
    {
        var url = "/bookmark/interested/" + id + "/";
    }
    
    $.post(url, function (result) {
        if (result == -1)
        {
            alert("Previously voted");
        }
        else
        {
            count.text(result);
        }
        
    }).fail(function(jqXHR, textStatus, errorThrown){
                alert("\ntextStatus: " + textStatus + "\nerrorThrown: " + errorThrown);});
    return false;
};

$(document).ready(function () {
    $(".interested").click(update_like_count);
});

function update_level_count(level) {
    var count = $(this).next();
    var id = $(this).attr("href").match(/\/bookmark\/level_vote\/([0-9]+)/)[1];
    var url = "/bookmark/level_vote/" + id + "/" + count.attr('class') + "/";
    $.post(url, function (result) {
        if (result == -1)
        {
            alert("Previously voted");
        }   
        else
        {
            count.text(result);    
        }
        
    }).fail(function(jqXHR, textStatus, errorThrown){
                alert("\ntextStatus: " + textStatus + "\nerrorThrown: " + errorThrown);});
    return false;
};

function path_bookmark_ids() {
    var ids = [];
    $("span.bookmark-id").each(function() {
        ids.push($(this).text());
    });
    return ids;

};

$(document).ready(function () {
    $(".beginner").click(update_level_count);
    $(".intermediate").click(update_level_count);
    $(".advanced").click(update_level_count);

    $("#path_bookmarks").bind( "mousedown", function (e) {
            e.metaKey = true;
    }).selectable({ filter: "article" });

    $("#sort-step").hide();
    $("#none-select").hide();


    $("#next_path").click(function () {

        // check that at least one bookmark is selected
        if($(".ui-selected").length > 1) 
        {
            $("#select-step").hide();
            $("#none-select").hide(); 
            $("#sort-step").show();
            $(".bookmark:not(.ui-selected)").remove();
            $('article').removeClass('thumbnail').addClass('thumbnail-draggable');
            $("#path_bookmarks").selectable("destroy");
            $('#path_bookmarks').isotope('destroy');
            $("#path_bookmarks").sortable();
            $("#path_bookmarks").disableSelection();
        }
        else
        {
            $("#none-select").show();          
        }
    });

    $("#next_path2").click(function (){
        alert(path_bookmark_ids());
        var url = "/path/save/" + 
                  "?ids=" + path_bookmark_ids();

        window.location.href = url;
        
        // $.ajax({
        //     url: url, 
        //     type: 'GET',
        //     data: { ids: [path_bookmark_ids()] },
        //     traditional: true
        // }).done(function() { alert("success"); });
    });

    // $("#edit_save_path").click(function () {
    //     var id =  
    //     var url = "/user/" + dj_request_user + "/path_save/" +
    //               "?edit=" + id;
    // });

});
