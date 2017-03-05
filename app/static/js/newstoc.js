document.addEventListener('DOMContentLoaded', function() {

    $('#api-news').prepend('<nav id="toc" class="well"><span class="text-muted">Summary</span></br></br></nav>')

    htmlTableOfContents();
} );

function htmlTableOfContents( documentRef ) {
    var documentRef = documentRef || document;
    var toc = documentRef.getElementById("toc");
    var main = $('#api-news')

    var headings = [].slice.call(main[0].querySelectorAll('h1, h2, h3, h4, h5, h6'));
    headings.forEach(function (heading, index) {
        var ref = "toc" + index;
        if ( heading.hasAttribute( "id" ) )
            ref = heading.getAttribute( "id" );
        else
            heading.setAttribute( "id", ref );

        var link = documentRef.createElement( "a" );
        // link.setAttribute( "href", "#"+ ref );
        $(link).on('click', function(e){
            var target = $('#' + ref )
            var parent = (IS_WITH_SIDEBAR) ? $('#content-with-sidebar') : $('body');
            scrollHelper(parent, target, true)
            urlHelper.updateParam('section', ref)
            e.preventDefault()
        })

        link.textContent = heading.textContent;

        var div = documentRef.createElement( "div" );
        div.setAttribute( "class", heading.tagName.toLowerCase() );
        div.appendChild( link );
        toc.appendChild( div );
    });
}
