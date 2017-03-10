var urlHelper = new function() {

  this.getUrl = function(){ return window.location.href };
  this.getUrlLocal = function(){ return window.location.pathname };
  this.getUrlParams = function(){ return window.location.search.substring(1) };
  this.getDecodedUrl = function() {decodeURIComponent(this.getUrl)};

  this.getParam = function(paramName) {
      var results = new RegExp('[\?&]' + paramName + '=([^&#]*)').exec(this.getDecodedUrl);
      if (results==null){
         return null;
      }
      else{
         return results[1] || 0;
      }
  }

  this.getParams = function() {
      // Returns all params in url as json object
      var uri = this.getUrlParams()

      var re = new RegExp('(&$|#$)')
      uri = uri.replace(re, '')
      var re = new RegExp('(&{2,})')
      uri = uri.replace(re, '&')
    //   this.pushUrl(uri)
    //   uri = uri.split('#')[0] // Remove, tripping parser, and not in use
      if (uri) {
          var jsonString = '{"' + decodeURI(uri).replace(/"/g, '\\"').replace(/[&?]/g, '","').replace(/=/g,'":"') + '"}'
          try {
              return JSON.parse(jsonString)
          }
          catch(e){
              console.log('ERROR PARSING: ' + jsonString)
          }
      }
      return {}
  }

  this.pushUrl = function(urlString) {
      history.pushState(null, null, urlString);
      return this.getUrl()
  }

  this.setToYear = function(year) {
      this.pushUrl('/' + year + '/')
  }

  this.updateParam = function updateParam(key, value) {
      var uri = this.getUrl()
      var newUrl = this._updateParam(uri, key, value)
      this.pushUrl(newUrl)
  }

  this._updateParam = function updateParam(uri, key, value) {
  // http://stackoverflow.com/questions/5999118/add-or-update-query-string-parameter
          // Sanitizes: clears double && and at end
          var re = new RegExp('(&$|#$)')
          uri = uri.replace(re, '')
          var re = new RegExp('(&{2,})')
          uri = uri.replace(re, '&')

          var re = new RegExp("([?&])" + key + "=.*?(&|#|$)", "i");
          if( value === undefined ) {
          	if (uri.match(re)) {
                uri = uri.replace(re, '$1$2');
                // uri = uri.replace(re, '');
        		return uri
        	} else {
        		return uri;
        	}
          } else {
          	if (uri.match(re)) {
          		return uri.replace(re, '$1' + key + "=" + value + '$2');
        	} else {
            var hash =  '';
            if( uri.indexOf('#') !== -1 ){
                hash = uri.replace(/.*#/, '#');
                uri = uri.replace(/#.*/, '');
            }
            var separator = uri.indexOf('?') !== -1 ? "&" : "?";
            return uri + separator + key + "=" + value + hash;
          }
          }
        }


};


// Updates a key-value on url parameter:
// URL: revitpythondocs.com/python/?query=3
// updateQueryStringParameter(query, '5')
// URL: revitpythondocs.com/python/?query=5
// function updateQueryStringParameter(key, value) {
//   var uri_parts = window.location.href.split('/')
//   var uri_local = uri_parts[uri_parts.length - 1]
//   var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
//   var separator = uri_local.indexOf('?') !== -1 ? "&" : "?";
//   if (uri_local.match(re)) {
//     return uri_local.replace(re, '$1' + key + "=" + value + '$2');
//   }
//   else {
//     return uri_local + separator + key + "=" + value;
//   }
// };
//
// // Extracts Decoded Param from url param
// function getUrlParam (name){
//     var url = decodeURIComponent(window.location.href)
//     var results = new RegExp('[\?&]' + name + '=([^&#]*)').exec(url);
//     if (results==null){
//        return null;
//     }
//     else{
//        return results[1] || 0;
//     }
// };
//
// function getUrlState (){
//     var url = decodeURIComponent(window.location.href)
//     var results = url.split('#')[1]
//     if ((results==null)||(results==0)){
//        return null;
//     }
//     else{
//        return results;
//     }
// };


// UrlHelper
// UrlHelper.pushUrl('Peido')
// console.log('Url:' + UrlHelper.getUrl)
// console.log('Decoded Url:' + UrlHelper.getDecodedUrl)
// UrlHelper.pushUrl('Peido Fedido')
// console.log('Url:' + UrlHelper.getUrl)
// console.log('Decoded Url:' + UrlHelper.getDecodedUrl)

// UrlHelper.pushUrl('?peido=fedido')
//var newUrl = UrlHelper.updateParam('peido', 'sussa', true)

// UrlHelper.getParam('peido')
// UrlHelper.getParam('non-existing-paramName')

//UrlHelper.updateParam('key', 'something2')
//UrlHelper.updateParam('key2', 'something2')
