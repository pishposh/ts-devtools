// current Global.* stuff here

(function (root, factory) {
  if (typeof define === 'function' && define.amd) {
    define([], factory); // AMD. Register as an anonymous module.
    
  } else {
    root.Global = factory(); // Browser globals
  }
}(this, function() {
  Global = {
    netDns: "https://w.taskstream.com/",
    IsDotNetHost: true
  };
  
  // Just return a value to define the module export.
  // This example returns an object, but the module
  // can return a function as the exported value.
  return Global;
}));
