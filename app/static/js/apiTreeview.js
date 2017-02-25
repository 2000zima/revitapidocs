$(document).ready(function() {

    //////////////////////////////
    /// NAMESPACE TREEVIEW AJAX //
    //////////////////////////////
    if (!is_mobile){
        // Load Menue, Desktop Only
        var ajaxNamespaceJson = $.getJSON("namespace.json", function(json) {
            var namespace_json = JSON.stringify(json);
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
        if (!is_small_screen && activeHref != null){
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

        else if (!is_small_screen) {
            $treeview.treeview('revealNode', [ 1, { silent: false } ]);
        };
        revealTreeview($treeview)

    return $treeview
    };
    // End of Build Menu Call Back Function

    ///////////////////////
    /// TREEVIEW HELPERS //
    ///////////////////////
    function revealTreeview($treeview) {
        // $('#menu-loading').fadeOut('fast')
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
    // $(document).on('click', '.node-treeview a', function(e){
    $(document).on('click', '.node-treeview a, #api-content a', function(e){
        // Use this to handle all links to load them ajax style
        var contenHref = $(this).attr('href')
        var hrefPattern = new RegExp('[A-Za-z0-9]{8}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{4}-[A-Za-z0-9]{12}.htm')

        if (!contenHref.match(hrefPattern)) { return true }

        e.preventDefault();

        var ajaxContent = $.getJSON( contenHref + '?ajax' , function(json) {
            $("#api-content-wrapper").html(loadingSpan)
            ajaxHelper.loadContent(json, false)
            ajaxHelper.updateYearNavStatus(json)
            UrlHelper.pushUrl(contenHref)
        });

        if (!is_mobile && !is_small_screen) {
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

            // TODO: Clicking here crashes node search > 2017.1/cba2c84a-22c0-e6e7-a99c-67656901853a.htm
        };
    });


// End of Doc Ready
 });
