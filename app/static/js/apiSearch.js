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
    $('.modal-title').html('Query: <strong>'+ query +'</strong>');
    $('#google-link').attr("href", "www.google.com/search?q=site:www.revitapidocs.com " + query)
    $('#modal-results').html(loadingSpan)
    $('#searchModal').modal('show');
    // $('#result-filter').html('')
    // var pushUrl = updateQueryStringParameter('filter', '');
    // urlHelper.pushUrl(clean_uri);
    // search(pattern, null, true)

    var resultsJson;
    var ajaxSearch = $.getJSON("search?query=" + query, function(json) {
        console.log('Search Ajax call successful. ')
        resultsJson = json;
        });
    ajaxSearch.done(function(){
        buildResults(resultsJson, query);
        var gaUrl = '/' + activeYear +'/?query=' + query
        ga('send', 'pageview', gaUrl);
    })
    ajaxSearch.fail(function(){
        console.log('Search Ajax call FAILED.')
        var resultsJson = {'error':' Could not reach search API'};
    })
};

function buildResults(resultsJson, query) {
    var modalResults = $('#modal-results')
    if (resultsJson.error) {
        modalResults.html('<p class="text-danger">' + resultsJson.error + '</p>')
    }
    else{
        // $.each(resultsJson) {

        function unwrapYears() {
           return function(years, render) {

               var yearsArr = []
               for (var key in years) {
                   yearsArr.push(key.toString())
               }
               return render(yearsArr.join(' / '))
            }
        }

        var results = {'results': resultsJson }
        modalResults.html( Mustache.to_html(resultEntryTemplate, results) );
        }
}
