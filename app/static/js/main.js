$(".alert").delay(8000).fadeOut(300, function() {
    $(this).alert('close');
});

$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
    // $('#alertTooltip').attr('title', "Tooltip new <br /> message").tooltip('fixTitle');
    // data-selector needed for tooltip bughttps://github.com/twbs/bootstrap/issues/15359 -->

});


function loadContent(contentJson, firstLoad) {
    $('.breadcrumb').first().html( Mustache.to_html(breadcrumb, contentJson) );

    if (firstLoad == true) {
        return
    }

    console.log('Loading content: ' + contentJson['content_path'])
    var contentHtml = contentJson['content_html']
    var years = contentJson['content_html']

    $('#api-title').html( contentJson['entry']['title'] );

    $("#api-content-wrapper").fadeOut(function() {
        $(this).scrollTop(0);
        $(this).html(contentHtml).fadeIn('slow');
    });

};

function updateYearNavStatus(contentJson) {
    var years = contentJson['entry']['years']
    $('#nav-main a').each(function(index, navLiTag) {
        var $navLiTag = $(navLiTag)
        var title = $navLiTag.attr('data-name')
        if (title != 'Python' && contentJson['entry']['years'])
        {
            // console.log('Adding: ' + $navLiTag.attr('title'))
            var year = $(navLiTag).attr('data-name')
            var status = years[year]
            if (!status) { status = 'missing'}

            $navLiTag.removeClass('exists')
            $navLiTag.removeClass('missing')
            $navLiTag.removeClass('updated')
            $navLiTag.removeClass('unchanged')
            $navLiTag.addClass(status)
            $navLiTag.attr({'title':''})
            if (status != 'exists') {
                $navLiTag.attr({'data-original-title':status})
            }
            if (year == contentJson['active_year']){
                var href = '/' + year
            }
            else {
                var href = '/' + year + '/' + contentJson['entry']['href']
            }
            $navLiTag.attr({'href': href})
        }
    })


};

// function getJson(url) {
//     var ajaxContent = $.getJSON(url, function(json) {
//         var contentJson = json
//
//     });
//         ajaxContent.done(function() {
//             console.log('! Content Loaded.');
//         });
//
//         ajaxNamespaceJson.fail(function(e) {
//             console.log('* Could load content');
//         });
//     }

// Updates a key-value on url parameter:
// URL: revitpythondocs.com/python/?query=3
// updateQueryStringParameter(query, '5')
// URL: revitpythondocs.com/python/?query=5
function updateQueryStringParameter(key, value) {
  var uri_parts = window.location.href.split('/')
  var uri_local = uri_parts[uri_parts.length - 1]
  var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
  var separator = uri_local.indexOf('?') !== -1 ? "&" : "?";
  if (uri_local.match(re)) {
    return uri_local.replace(re, '$1' + key + "=" + value + '$2');
  }
  else {
    return uri_local + separator + key + "=" + value;
  }
};

// Extracts Decoded Param from url param
function getUrlParam (name){
    var url = decodeURIComponent(window.location.href)
    var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(url);
    if (results==null){
       return null;
    }
    else{
       return results[1] || 0;
    }
};

function getUrlState (){
    var url = decodeURIComponent(window.location.href)
    var results = url.split('#')[1]
    if ((results==null)||(results==0)){
       return null;
    }
    else{
       return results;
    }
};
