$(document).ready(function() {

    var $searchBoxInput = $('#search-box')
    ajaxHelper.createConstructor($searchBoxInput, CONSTRUCTOR_KEY, 10)
    console.log('here')

    $("#sidebar-search > form").submit(function(e) {
        e.preventDefault() // Keeps page from submitting and reloading
        var query = $searchBoxInput.val();
        submitSearch(query)

    });
});

function submitSearch(query) {
    $('#modal-results').html(loadingSpan)
    $('#searchModal').modal('show');
    // $('#result-filter').html('')
    // var pushUrl = updateQueryStringParameter('filter', '');
    // urlHelper.pushUrl(clean_uri);

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
    if (resultsJson.error) {
        $modalResults.html('<p class="text-danger">' + resultsJson.error + '</p>')
    }
    else{
        var source   = $("#result-entry-template").html();
        var template = Handlebars.compile(source);

        // var results = {'results': resultsJson }
        var html = template(resultsJson);
        $modalResults.html(html);

        }

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
