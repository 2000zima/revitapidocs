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

        console.log('Loading content: ' + contentJson['content_path'])
        var contentHtml = contentJson['content_html']
        var years = contentJson['content_html']

        $('#api-title').html( contentJson['entry']['title'] );

        $("#api-content-wrapper").fadeOut(function() {
            $(this).scrollTop(0);
            $(this).html(contentHtml).fadeIn('slow');
        });

    };

    ///////////////////////////
    /// UPDATE NAV BAR YEARS //
    ///////////////////////////
    this.updateYearNavStatus = function(contentJson) {
        var years = contentJson['entry']['years']
        $('#nav-main a').each(function(index, navLiTag) {
            var $navLiTag = $(navLiTag)
            var title = $navLiTag.attr('data-name')
            if (title != 'Python' && contentJson['entry']['years']) {
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
    this.createConstructor = function($inputbox, CONSTRUCTOR_KEY, maxResults) {
        $.getScript("//cnstrc.com/js/ac.js", function() {
                $inputbox.constructorAutocomplete({
                key: CONSTRUCTOR_KEY,
                boostRecentSearches : true,
                maxResults : maxResults,
                triggerSubmitOnSelect: true
                });
        });
    }
};
