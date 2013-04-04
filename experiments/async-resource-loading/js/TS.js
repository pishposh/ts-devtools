/*
 *  current TS.* functionality
 */

// github.com/umdjs/umd

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    // AMD. Register as an anonymous module.
    define(['jquery', 'JqAjaxTsTunnel'], factory);
    
  } else {
    // Browser globals
    root.TS = factory(root.jQuery);
  }
}(this, function($, jqAjaxTsTunnel) {
  TS = { hello: true };
  
  window.console && console.log(jqAjaxTsTunnel);
  
  $(function(){
    $("#dynamic-content").append("<p>Hello from TS.js!</p>");
  });
  
  return TS;
}));
