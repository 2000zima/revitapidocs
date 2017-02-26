var urlHelper = new function() {

  // getUrl: Something%20With%20Space
  this.getUrl = window.location.href;
  this.getUrlPath = window.location.pathname;
  // getDecodedUrl: Something With Space
  this.getDecodedUrl = decodeURIComponent(this.getUrl);

  this.getParam = function(paramName) {
      var results = new RegExp('[\?&]' + paramName + '=([^&#]*)').exec(this.getUrl);
      if (results==null){
         return null;
      }
      else{
         return results[1] || 0;
      }
  }

  this.getParams = function() {
      this.params = {}
      this.params.query = this.getParam('query')
      this.params.filter = this.getParam('filter')
  }

  this.pushUrl = function(urlString, append=false) {
      if (append) { urlString += this.getUrl };
      history.pushState(null, null, urlString);
      return this.getUrl
  }

  this.updateParam = function(key, value, push=true) {
      var uri_parts = this.getDecodedUrl.split('/')
      var uri_local = uri_parts[uri_parts.length - 1]
      var re = new RegExp("([?&])" + key + "=.*?(&|$)", "i");
      var separator = uri_local.indexOf('?') !== -1 ? "&" : "?";
      if (uri_local.match(re)) {
        var new_uri = uri_local.replace(re, '$1' + key + "=" + value + '$2');
      }
      else {
        var new_uri = uri_local + separator + key + "=" + value;
      }
      if (push) {
          this.pushUrl(new_uri);
      }
  }
}


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
