$(document).ready(function() {

    var $searchBoxInput = $('#search-box')
    ajaxHelper.createConstructor($searchBoxInput, CONSTRUCTOR_KEY, 10)

    $("#sidebar-search > form").submit(function(e) {
        e.preventDefault() // Keeps page from submitting and reloading
        var query = $searchBoxInput.val();
        submitSearch(query)
    });

});

function submitSearch(query) {

    var alertLoading = flashAlert('Loading')
    urlHelper.updateParam('query', query)

    var resultsJson;
    var ajaxSearch = $.getJSON("search?query=" + query, function(json) {
        console.log('Search Ajax call successful. ')
        resultsJson = json;
        });
    ajaxSearch.done(function(){
        var gaUrl = '/' + activeYear +'/?query=' + query
        ga('send', 'pageview', gaUrl);
    })
    ajaxSearch.fail(function(){
        console.log('Search Ajax call FAILED.')
        resultsJson = {'error':' Could not reach search API'};
    })
    ajaxSearch.always(function(){
        buildResults(resultsJson, query);
    })
};

function buildResults(resultsJson, query) {
    var $modalResults = $('#modal-results')
    var source   = $("#modal-template").html();
    var template = Handlebars.compile(source);
    var html = template(resultsJson);
    $modalResults.html(html);

    $('.alert').hide();
    $('#searchModal').modal('show');

    var urlParams = urlHelper.getParams()
    if (urlParams.filter) { toggle_tag(urlParams.filter) }
    if (urlParams.scroll) {
        scrollHelper($('.modal-body'), urlParams.scroll, false, 0)
    }

    // SHOW TRUNCATED WARNING
    var maxResults = resultsJson['max_results']
    var totalResults = resultsJson['total_results']
    if (totalResults >= maxResults) {
        var alertResults = flashAlert('Results truncated to '+maxResults, 'danger')
        alertResults.delay(6000).fadeOut('slow')
    }

    bindToModalElements()
};

// Toggle Tag Filter Function
function toggle_tag(tag_name){

    // var activeTagName = $('#result-filter').text()
    var activeTagName = urlHelper.getParams().filter


    if (activeTagName == tag_name){
        var $filterBox = $('#result-filter-box')
        var tagNamePat = new RegExp('(\\s+)?' + tag_name, 'i')
        $filterBox.val($filterBox.val().replace(tagNamePat, ''))
        // $('#result-filter-box').val(tag_name)
        $('.result-entry[data-tag!="' + tag_name + '"]').show();
        urlHelper.updateParam('filter', undefined)
    }

    else {
        // No Tag Active, Toggle On
        var $filterBox = $('#result-filter-box')
        var space = $filterBox.val() == '' ? '' : ' '
        $filterBox.val($filterBox.val() + space + tag_name)
        // $('#result-filter').html(tag_name)
        $('.result-entry[data-tag!="' + tag_name + '"]').hide();
        urlHelper.updateParam('filter', tag_name)
    }

    filterResults()
};


function filterResults(){
    $filterBox = $('#result-filter-box')
    var valThis = $filterBox.val();
    $('.result-entry').each(function(){
        var title = $(this).find('h5>a').text();
        // var desc = $(this).find('.description').text();
        var words = valThis.split(' ')
        var combined = words.join('.+')
        pat = new RegExp(combined, 'i')

        if (title.match(pat)) {
        // if ( (title.match(pat)) || (desc.match(pat)) ) {
            $(this).show();
        }
        else{
            $(this).hide()
        }
    });
};

function bindToModalElements(){

    // ON SCROLL
    $(".modal-body").on('scroll', function(){
        if ($(this).scrollTop() > 1){ $(this).addClass("bottom-shadow") }
        else {$(this).removeClass("bottom-shadow")}

        var result_scroll = $(".modal-body").scrollTop()
        urlHelper.updateParam('scroll', result_scroll)
    })

    // ON MODAL CLOSE
    $('.modal').on('hidden.bs.modal', function (event) {
        urlHelper.setToYear(activeYear)
        $('search-box').focus()
    });

    // ON TAG CLICK
    $('.result-tag').on('click', function(e){
      var tag_name = $(this).text()
      toggle_tag(tag_name)
    });

    $('#result-filter-box').keyup(function(){
        filterResults()
    });
}


//////////////////////////
// HANDLE BARS HELPERS ///
//////////////////////////

Handlebars.registerHelper('joinyears', function(options) {
    var years = this.years
    var yearsArr = []
    for (var year in years) {
        yearsArr.push(year)
    }

    if (yearsArr.length === 4){ return 'All years' }
    var cls
    if (yearsArr.indexOf(options.data.root['target_year']) == -1) {
        var cls = 'missing'
    }
    return '<span class="'+cls+'">' + yearsArr.join(' / ') + '</span>'
});

Handlebars.registerHelper('exactMatch', function(options) {
    var query = options.data.root['query'].toLowerCase()
    var title = this.title.toLowerCase()
    if (query == title) {
        return 'result-exact-match'
    }
});
