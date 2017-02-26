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

window.addEventListener('popstate', function(event) {
    // Check Url from when using back button but staying on the same page
    location.reload(urlHelper.getUrl)
});


$(".alert").delay(8000).fadeOut(300, function() {
    $(this).alert('close');
});


$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();

    /////////////////////////////
    // SIDEBAR SEARCH SCROLL  ///
    /////////////////////////////
    $("#sidebar").scroll(function(){
      if ($("#sidebar").scrollTop() > 1){
          $("#sidebar-search").css("top", $("#sidebar").scrollTop() + 0 + "px");
          $("#sidebar-search").addClass("bottom-shadow")

      } else {
          $("#sidebar-search").css("top", "0px");
          $("#sidebar-search").removeClass("bottom-shadow")
      }
    });

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
