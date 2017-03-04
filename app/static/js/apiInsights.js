$(document).ready(function() {
    if (!$('#exampleSection')[0]) {
        return
    }

    var query = templateData['entry']['short_title']
    var url = "/api/insights?query=" + query

    var results
    var ajaxInsights = $.getJSON(url, function(json) {
        results  = json
        console.log('Examples present. Getting Python example...')
    })

    ajaxInsights.done(function() {
        addInsight(results, query)
    })


});

function addInsight(results, query) {
    var match = { 'results' : results,
                  'query': query }
                 //  'href': items[0]['html_url'],
                 //  'repo': items[0]['repository']['name'] + ':' + items[0]['repository']['owner']['login']

    var source  = $("#code-template").html();
    var template = Handlebars.compile(source);
    var html = template(match);
    $('#exampleSection').append(html)

}
