$(document).ready(function() {

    // ////////////////////////////
    //  NAMESPACE TREEVIEW AJAX //
    // ////////////////////////////
    if (!IS_MOBILE && activeYear){
        // Load Menue, Desktop Only
        var ajaxNamespaceJson = $.getJSON("namespace.json", function(json) {
            var namespace_json = JSON.stringify(json)
            buildTreeView(namespace_json)
        });

        // Needs fail handling
        ajaxNamespaceJson.done(function() {
            console.log('Ajax JSON namespace loaded.');
            });

        ajaxNamespaceJson.fail(function() {
            console.log('Could not get namespace.json.');
            $('#menu-loading').html('Error Loading Namespace')
            });
    };

}); // End of Doc Ready

///////////////////////////////
/// BUILD NAMESPACE TREEVIEW //
///////////////////////////////
function buildTreeView(namespace_json) {

    var $treeview = $('#treeview').treeview({
          expandIcon: "node-icon collapsed",
          collapseIcon: "node-icon expanded",
          emptyIcon: "node-icon empty",
          selectedBackColor: "#21a3a3",
          selectedColor: "#fff",
          selectionAllowed: false,
          showBorder: false,
          levels: 1,
          enableLinks: true,
          highlightSelected: true,
          multiSelect: false,
          onhoverColor: '#e0e0e0',
          backColor: 'inherit',
          data: namespace_json
        })
    $treeview.hide();


    /////////////////////////////////////////////
    // Iterate nodes, try to match active_href //
    /////////////////////////////////////////////
    if (!IS_SMALL_SCREEN && activeHref != null){
        console.log('active_href is not None. Iterating to find matching href');

        var activeNodeId = findNodeIdByHref($treeview, activeHref)

        // Find Node, Expand, Select, and Scroll to it
        if (activeNodeId){
            console.log('Found Node.')
            $treeview.treeview('revealNode', [ activeNodeId, { silent: false } ]);
            $treeview.treeview('toggleNodeSelected', [ activeNodeId, { silent: false } ]);
            $treeview.treeview('toggleNodeExpanded', [ activeNodeId, { silent: false } ]);

            revealTreeview($treeview)
            scrollToNode(activeNodeId)
        }
    }

    else if (!IS_SMALL_SCREEN) {
        $treeview.treeview('revealNode', [ 1, { silent: false } ]);
    };
    revealTreeview($treeview)

return $treeview

};
// End of Build Menu Call Back Function

///////////////////////
/// TREEVIEW HELPERS //
///////////////////////
function revealTreeview ($treeview) {
    // $('#menu-loading').fadeOut('fast'),
    $('#menu-loading').hide();                    // Hide Loading
    $treeview.fadeIn('slow');    // Reveal Menu
    $('#treeview').animate({opacity: 1},'slow');    // Reveal Menu
};

function scrollToNode(nodeId) {
    var node = document.querySelectorAll('[data-nodeId="' + nodeId + '"]')[0];
    var elPosition = node.offsetTop;
    var scrollto = elPosition - 100
    $('#sidebar').scrollTop(scrollto); // Scroll, no animation
};

function findNodeIdByHref ($treeview, href) {

    var node
    var nodeId = 0;
    do {
        node = $treeview.treeview("getNode", nodeId);
        if (node && node.href == href) {
            return node.nodeId
        };
        nodeId++;
    }
    while (node.nodeId != undefined);

    return null
}

////////////////////////
// On Tree href click //
////////////////////////
// This handles <a> clicking outside, but keeping it here because
// logic is tightly integrated with treevie
// $(document).on('click', '.node-treeview a', function(e){
$(document).on('click', '.node-treeview a, #api-content a', function(e){

    var contenHref = $(this).attr('href')
    var hrefPattern = new RegExp('[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}.htm')

    if (!contenHref.match(hrefPattern)) { return true }

    e.preventDefault();

    var ajaxContent = $.getJSON( contenHref + '?ajax' , function(json) {
        $("#api-content-wrapper").html(loadingSpan)
        ajaxHelper.loadContent(json, false)
        ajaxHelper.updateYearNavStatus(json)
        urlHelper.pushUrl(contenHref)
    });

    if (!IS_MOBILE && !IS_SMALL_SCREEN) {
        var $treeview = $('#treeview')
        var nodeId = $(this).parent().attr('data-nodeId')
        var isMainContentClick // Click came from main div

        if (!nodeId) {
            var isMainContentClick = true
            var nodeId = findNodeIdByHref($treeview, contenHref)
        }

        var node = document.querySelectorAll('[data-nodeId="' + nodeId + '"]')[0];
        if (!node) {
            // If node is not visible, reload windows
            // Trying to expand it it's too intensive
            // and slows down browser
            location.reload();
        }

        $treeview.treeview('selectNode', [ Number(nodeId), { silent: false } ]);
        $treeview.treeview('expandNode', [ Number(nodeId), { silent: false } ]);

        if (isMainContentClick) {
            // $treeview.treeview('revealNode', [ Number(nodeId), { silent: false } ]);
            scrollToNode(nodeId)
        };
    };
});
