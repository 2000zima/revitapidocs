$(document).ready(function(e){

    var $searchBoxInput = $('#search-box')
    // Set Input
    $searchBoxInput.delay(1500).fadeIn(function() {
      $(this).focus();
    });

    // Typying Animation
    // Conditional Statement makes it so animation only runs the first time
    if (!localStorageHelper.get('revitapidocs_year')){
        $(function(){
          $('#direct-search input').typed({
            strings: ["Wall Class", "Pushbutton", "Global Parameter",
            "Idling Event", "Ribbon Item", "CreateBound", "ViewSchedule",
            "ViewType", "Revit.UI", "ActiveDocument", "DocumentClass",
            "BuiltinParameter", "Transaction Mode", "Element",
            "ElementId"],
            typeSpeed: 50,
            startDelay: 2500,
          });
        });
        $searchBoxInput.typed.isRunning = true
    }
    else {
        $searchBoxInput.attr({'Placeholder':'Search Term'})
        $searchBoxInput.typed.isRunning = false
    }

    // On First Click only, Clear Animation
    $searchBoxInput.one('click', function(){
      if ($searchBoxInput.typed.isRunning) {
          $searchBoxInput.typed('stops')
          $searchBoxInput.val('')
          $searchBoxInput.attr({'Placeholder':'Search Term'})
      }
    })

    // Clears Error when user clicks on input again
    $searchBoxInput.on('click', function(){
      $("div#direct-search").find('.form-group').removeClass('has-error')
      $("div#direct-search").find('.control-label').html("&nbsp;")
    })

    // Get Stored year
    var year = localStorageHelper.get('revitapidocs_year')
    if(year && (year != undefined)){
      var year = localStorageHelper.get('revitapidocs_year');
      $('button#direct-search-year').attr('value', year)
      $('span#dropdown-label').text(year)
    }
    else{
      localStorageHelper.set('revitapidocs_year', '2018');
      year = '2018'
    }

    // Initialize Constructor IO with default or stored year
    console.log('Calling Constructor. Year: '+ year)
    ajaxHelper.createConstructor($searchBoxInput, 5, year)

    // Select Item from dropdown
    $('#direct-search li').on('click', function(){
        var year = $(this).text()
        $('span#dropdown-label').text(year)
        $('button#direct-search-year').attr('value', year)
        $("button#direct-search-year").removeClass('btn-danger')
        $("div#direct-search").find('.form-group').removeClass('has-error')
        $("div#direct-search").find('.control-label').html("&nbsp;")

        localStorageHelper.set('revitapidocs_year', year);

        console.log('Recreating Constructor. Year: '+ year)
        // Restart Constructor IO with new Year
        ajaxHelper.createConstructor($searchBoxInput, 5, year)

    })

    function search(query, year){
      var searchUrl = '/' + year + '/?query=' + query
      window.location.href = searchUrl;
    }

    // Form Submit Handler
    $("#direct-search").submit(function(e) {
      e.preventDefault() // Keeps page from submitting and reloading
      var year = $('#direct-search-year').attr('value')
      var query = $searchBoxInput.val()

      if (year === 'UNDEFINED'){
        $("#direct-search").find('.form-group').addClass('has-error')
        $("#direct-search").find('.control-label').text('Select a year')
        $("#direct-search-year").addClass('btn-danger')
      }
      else if (query.length<2) {
        $("#direct-search").find('.form-group').addClass('has-error')
        $("#direct-search").find('.control-label').text('Search term is too short')
      }
      else {
        search(query, year)
      }
    });

    // Sections Toggle
    $('#toggle-contribute').on('click', function(){
      $('#contribute').slideToggle()
    })
    $('#toggle-other-resources').on('click', function(){
      $('#other-resources').slideToggle()
    })

});
