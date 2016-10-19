// Catch CHM script call
function OpenSection(sectionToggleName) {
  console.log(sectionToggleName)
  console.log(typeof(sectionToggleName))
  // var sectionName = sectionToggleName.replace('Toggle', 'Section')
  console.log(sectionName)
  var position = $('div'+sectionName).position().top
  $('#main-sidebar').scrollTop(position);
}
