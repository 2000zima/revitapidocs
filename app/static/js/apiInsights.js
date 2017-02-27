$(document).ready(function() {
    if (!$('#exampleSection')[0]) {
        return
    }

    var query = templateData['entry']['short_title']
    var users = ['gtalarico', 'eirannejad']


    var url = "/api/insights?query=" + query + '&user=gtalarico'

    var results
    var results2

    var ajaxInsights = $.getJSON(url, function(json) {
        results  = json
        console.log('Trying python repo 1...')
    })

    ajaxInsights.done(function() {
        if (results && results['total_count'] > 0) {
            console.log('Success.Adding Code...')
            addInsight(results)
        }
        else{
            console.log('No Results. Trying repo2...')
            var url = "/api/insights?query=" + query + '&user=eirannejad'
            var ajaxInsights2 = $.getJSON(url, function(json) {
            results2  = json
            })
            ajaxInsights2.done(function(){
                if (results2 && results2['total_count'] > 0) {
                console.log('Found it. Adding code...')
                addInsight(results2)
                }
                else {
                    console.log('No Results.')
                }
            })
        }
    });

});

function addInsight(json) {
    var items = json['items']
    var title = templateData['entry']['short_title']
    var match = {
                 'language': 'Python',
                 'code': items[0]['text_matches'][0]['fragment'],
                 'href': items[0]['html_url'],
                 'repo': items[0]['repository']['name'] + ':' + items[0]['repository']['owner']['login']
                 }

    var source  = $("#code-template").html();
    var template = Handlebars.compile(source);
    var html = template(match);
    $('#exampleSection').append(html)

}
