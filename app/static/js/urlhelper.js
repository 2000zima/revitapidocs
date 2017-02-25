var UrlHelper = new function() {

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
