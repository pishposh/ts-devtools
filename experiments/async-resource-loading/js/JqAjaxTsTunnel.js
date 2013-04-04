/**
 *  current: $.initAjaxTsTunnel(function(){ $.ajax(...sync or async...) })
 *
 *  todo:
 *  init frame automatically for async $.ajax requests, complain to devs about sync requests
 *  
 *  $.initAjaxAspToNet().then(function(){
 *      ...show page to user...
 *  })
 *
 *  $.initAjaxAspToNet().then(function(){
 *      $.ajax("//w.taskstream.com/...", ...)
 *  })
 */

// github.com/umdjs/umd
 
// Uses AMD or browser globals to create a jQuery plugin.

// It does not try to register in a CommonJS environment since
// jQuery is not likely to run in those environments.
// See jqueryPluginCommonJs.js for that version.

(function(factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['jquery', 'Global'], factory);
  } else {
    // Browser globals
    factory(jQuery, Global);
  }
}(function($, Global) {
  var tunnelIframe,
    tunnelCallbacks = [],
    initDeferred = $.Deferred();
  
  $.initAjaxTsTunnel = function(callback) {
    var netDns = (Global.netDns || Global.Links.netDns).replace(/\/$/,""); // strip trailing slash, if present
    
    // only load for IE and similar, only if not already installed, and only if we're not on .NET host
    if ($.support.cors || Global.IsDotNetHost) {
      // $.support.cors is also true after we've installed ourselves
      if (typeof callback === "function")
        callback();
      return initDeferred.resolve().promise();
    }
    
    // iframe isn't yet loaded, so queue callback to run later:
    if (typeof callback === "function")
      tunnelCallbacks.push(callback);
    
    // if iframe is already loading, just return now
    if (tunnelIframe)
      return initDeferred.promise();
    
    tunnelIframe = $("<iframe></iframe>")
      .attr("src", netDns + "/XhrTunnelShim")
      .on("load", installXhrOverride)
      .appendTo("head")[0];
    
    return initDeferred.promise();
    
    
    
    
    function installXhrOverride() {
      var xhrOrig = $.ajaxSettings.xhr,
        tunnelWindow = tunnelIframe.contentWindow;
      
      $.ajaxSettings.xhr = function() {
        var xhr;
        
        // use XMLHttpRequest/ActiveXObject from the other site, if appropriate:
        if (this.crossDomain && !this.isLocal && this.url.indexOf(netDns + "/") === 0) {
          
          // Temporarily swap out our local window's XHR objects with the tunnel's XHR objects,
          // letting jQuery's original xhr() choose between XMLHttpRequest and ActiveXObject.
          // We could also have just reimplemented xhr() here in its entirety, but that feels
          // less forwards-compatible with new jQueries.
          
          var savedXMLHttpRequest = window.XMLHttpRequest,
            savedActiveXObject = window.ActiveXObject;
          
          window.XMLHttpRequest = tunnelWindow.XMLHttpRequest;
          window.ActiveXObject = tunnelWindow.ActiveXObject;
          
          xhr = xhrOrig.apply(this, arguments);
          
          window.XMLHttpRequest = savedXMLHttpRequest;
          window.ActiveXObject = savedActiveXObject;
          
        } else {
          // return whatever original function would've:
          xhr = xhrOrig.apply(this, arguments);
        }
        
        return xhr;
      };
      
      $.support.cors = true;
      
      // fifo through callbacks:
      var callback;
      while (callback = tunnelCallbacks.shift())
        callback();
      initDeferred.resolve();
    }
  }
  
}));



