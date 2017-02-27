$(document).ready(function(){

    // Default
    var language = 'All'
    // Get Stored year
    if(localStorageHelper.get('dev_lanuage')){
      var language = localStorageHelper.get('dev_lanuage');
      $('#language-active').text(language)
    }
    else {
        localStorageHelper.set('dev_lanuage', language);
    }
    filterLanguage(language);


    // Select Item from dropdown
    $('.language-selector').on('mousedown', function(){
      var language = $(this).text()
      $('#language-active').text(language)
      localStorageHelper.set('dev_lanuage', language);

      filterLanguage(language);
    })


})

function filterLanguage(language) {
    var languages = {'C#':'CSharp',
                     'VB':'VisualBasic',
                     'C++':'ManagedCPlusPlus',
                     'Python':'Python'
                    }
    var setLanguage = localStorageHelper.get('dev_lanuage')
    var languageClass = languages[setLanguage]
    if (setLanguage == 'All') {
        $('#syntaxCodeBlocks, #exampleSection').children().show()
    }
    else {
        $('#syntaxCodeBlocks, #exampleSection').children('span[codelanguage!="' + languageClass +'"]').hide()
        $('#syntaxCodeBlocks, #exampleSection').children('span[codelanguage*="' + languageClass +'"]').show()
    }
}
