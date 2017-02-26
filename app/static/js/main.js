/////////////
// GLOBALS //
/////////////
var activeYearPattern = new RegExp('(?:/)([0-9\.]{4,6})(?:/)');
var activeYear = window.location.pathname.match(activeYearPattern);
activeYear = (activeYear) ? activeYear[1] : null

var activeHrefPattern = new RegExp('(?:/[0-9\.]{4,6}/)([A-Za-z0-9\-]*.htm)')
var activeHref = window.location.pathname.match(activeHrefPattern)
activeHref = (activeHref) ? activeHref[1] : null

var IS_MOBILE = ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
var IS_SMALL_SCREEN = ($(window).width() < 768);
var IS_WITH_SIDEBAR = !IS_MOBILE && ! IS_SMALL_SCREEN

$(window).resize(function(){
    var IS_SMALL_SCREEN = ($(window).width() < 768);
    var IS_WITH_SIDEBAR = !IS_MOBILE && !IS_SMALL_SCREEN
    if (!IS_WITH_SIDEBAR) {
        // Patch for when window is resized small after quick search is on
        $("#sidebar-search").css("top", "0px");
        $("#sidebar-search").removeClass("bottom-shadow")
        }
})


window.addEventListener('popstate', function(event) {
        location.reload(urlHelper.getUrl);
});


$(".alert").delay(8000).fadeOut(300, function() {
    $(this).alert('close');
});


$(document).ready(function() {
    // Enable Tooltips
    $('[data-toggle="tooltip"]').tooltip();


    ///////////////////////////////
    // COPY PASTE CODE EXAMPLES ///
    ///////////////////////////////
    $('.highlight-copycode').click(function(){
        var $code = $(this).parent().next()

        if (document.selection) {
            var range = document.body.createTextRange();
            range.moveToElementText($code[0]);
            range.select();
        } else if (window.getSelection) {
            window.getSelection().removeAllRanges();
            var range = document.createRange();
            range.selectNode($code[0]);
            window.getSelection().addRange(range);
        }

        var succeed;
        try {
            succeed = document.execCommand("copy");
        } catch (e) {
            succeed = false;
        }
        if (succeed) {
            $(this).attr({'title':'Copied'})
            $(this).tooltip('show')
        }

        $(this).attr({'data-original-title':''})

    });

});

// FLASH HELPER
function flashAlert(text, style='info') {
    var alertBox = '<div class = "alert alert-'+style+'" role="alert">' +
                   '<button type="button" class="close" data-dismiss="alert" aria-label="Close">' +
                   '<span aria-hidden="true">&times;</span></button>' +
                   '</div>'

    $('#content-wrapper').append(alertBox)
    $('.alert').append(text)
    return $('.alert')
}

// SCROLL HELPER
function scrollHelper(parent, anchor, animate, offset=75){

    if (typeof(anchor) == 'string') {
        var targetScrollTop = Number(anchor)
    }
    else {
        var targetScrollTop = anchor.offset().top - offset
    }

    if (animate) {
        parent.animate({scrollTop: targetScrollTop},'slow');
    }
    else {
        parent.scrollTop(targetScrollTop - offset)
    }
}

var localStorageHelper = new function() {
    this.set = function(key, value){
        if (localStorage){
            localStorage.setItem(key, value);
            return true
        }
    }

    this.get = function(key){
        if (localStorage){
            return localStorage.getItem(key);
        }
    }
}
