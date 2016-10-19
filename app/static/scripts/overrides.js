// Catch CHM script call to toggle section
function OpenSection(sectionToggleName) {
  var scrollTo = $(sectionToggleName).parent().position().top
  console.log(scrollTo)
  $('#main-sidebar').animate({ scrollTop: scrollTo - 20 }, 400, "swing");
  // $('#main-sidebar').scrollTop(scrollTo);
}
