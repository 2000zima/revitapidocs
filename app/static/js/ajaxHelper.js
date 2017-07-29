var ajaxHelper = new function() {
    ///////////////////////////////
    /// LOAD CONTENT DYNAMIcALLY //
    ///////////////////////////////
    this.loadContent = function(contentJson, firstLoad) {
        // $('.breadcrumb').first().html( Mustache.to_html(breadcrumbTemplate, contentJson) );
        var source   = $("#breadcrumb-template").html();
        var template = Handlebars.compile(source);
        var html = template(contentJson);
        $('.breadcrumb').first().html(html);

        if (firstLoad == true) {
            return
        }
        var $apiContentWrapper = $("#api-content-wrapper")
        $apiContentWrapper.html(loadingSpan)
        $('#api-title').html( contentJson['entry']['title'] );

        console.log('Loading content: ' + contentJson['content_path'])
        var contentHtml = contentJson['content_html']
        var years = contentJson['content_html']


        $apiContentWrapper.scrollTop(0);
        $apiContentWrapper.html(contentHtml)
        // $apiContentWrapper.hide(function() {
        //     $(this).scrollTop(0);
        //     $(this).html(contentHtml).show();
        //     $(this).html(contentHtml).fadeIn('slow');
        // });

    };

    ///////////////////////////
    /// UPDATE NAV BAR YEARS //
    ///////////////////////////
    this.updateYearNavStatus = function(contentJson) {
        var years = contentJson['entry']['years']
        $('#nav-main a.api-button').each(function(index, navLiTag) {
            var $navLiTag = $(navLiTag)
            var title = $navLiTag.attr('data-name')
            if (title != 'Code Samples' && contentJson['entry']['years']) {
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
                // if (status != 'exists') {
                    $navLiTag.attr({'data-original-title':status})
                // }
                if (year == contentJson['active_year']){
                    var href = '/' + year
                }
                else {
                    var href = '/' + year + '/' + contentJson['entry']['href']
                }
                $navLiTag.attr({'href': href})
            };
        });
    };

    ///////////////////////////
    /// CONSTRUCTOR.IO AJAX  //
    ///////////////////////////
    this.createConstructor = function($inputbox, maxResults, year) {

      var key = localStorageHelper.get('CONSTRUCTOR_KEY')

      if (key != undefined){
        console.log('Storage Key found')
         create(key)
      }
      else {
        var getKey = $.getJSON('/api/constructor_key', function(json) {
            console.log('Key not found. Fetching...')
            var key = json

            getKey.done(function(){
              console.log('Key not found. Fetching...')
              localStorageHelper.set('CONSTRUCTOR_KEY', key)
              create(key)
            });
        });
      }

      function create(CONSTRUCTOR_KEY) {

          var constructor = $.getScript("//cnstrc.com/js/ac.js", function() {
                  $inputbox.constructorAutocomplete({
                  key: CONSTRUCTOR_KEY,
                  boostRecentSearches : true,
                  maxResults : maxResults,
                  triggerSubmitOnSelect: true,
                  directResultUrlPrefix: '/' + year + '/',
                  onSearchComplete: function(name, suggestions,c,d){

                      $('.autocomplete-suggestion').each(function(index){

                        if (!$(this).children('.autocomplete-suggestion-description')[0]) {
                          $(this).append('<span class="autocomplete-suggestion-description"></span>')
                        }

                        // Wraps loose text in span
                        $(this).children('span').wrapInner('<span class="description"></span>')

                        // Wraps loose text in span
                        var $memberOf = $('<span class="member-of"></span>')
                        $memberOf.text(suggestions[index].data['member_of'])
                        $(this).children('span').prepend($memberOf)



                      })
                  }
                  });
          });
      }
    }
};
