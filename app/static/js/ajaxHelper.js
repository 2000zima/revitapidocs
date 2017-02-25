var ajaxHelper = new function() {

    this.loadContent = function(contentJson, firstLoad) {
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
};
