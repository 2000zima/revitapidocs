$(document).ready(function() {
    if (!$('#exampleSection')[0]) {
        return
    }

    var query = templateData['entry']['short_title']
    var url = "/api/insights?query=" + query

    var response
    var ajaxInsights = $.getJSON(url, function(json) {
        response  = json
        console.log('Examples present. Getting Python example...')
    })

    ajaxInsights.done(function() {
        addInsight(response, query)
    })


});

function addInsight(response, query) {
    var match = { 'results' : response['results'],
                  'url': response['url'],
                  'query': query }

    var source  = $("#code-template").html();
    var template = Handlebars.compile(source);
    var html = template(match);
    $('#exampleSection').append(html)

}
