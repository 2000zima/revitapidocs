$(".alert").delay(8000).fadeOut(300, function() {
    $(this).alert('close');
});

$(document).ready(function() {
    $('[data-toggle="tooltip"]').tooltip();
});

// GLOBALS
var activeYearPattern = new RegExp('(?:/)([0-9\.]{4,6})(?:/)')
var activeYear = window.location.pathname.match(activeYearPattern)[1]
console.log('activeYear: ' + activeYear)

var activeHrefPattern = new RegExp('(?:/[0-9\.]{4,6}/)([A-Za-z0-9\-]*.htm)')
var activeHref = window.location.pathname.match(activeHrefPattern)
activeHref = (activeHref) ? activeHref[1] : null

console.log('activeHref: ' + activeHref)

var is_mobile = ( /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent));
console.log('is_mobile: ' + is_mobile)

var is_small_screen = ($(window).width() < 768);
console.log('is_small_screen: ' + is_small_screen)
