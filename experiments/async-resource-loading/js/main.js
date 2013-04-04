require.config({
  paths: { 
    "jquery": "lib/jquery-1.9.1"
  }
});

require(["TS", "jquery"], function(TS, $) {
  
  $(function(){
    $("#dynamic-content").append("<p>Hello from main.js, where TS.hello is " + TS.hello + "!</p>");
  });
  
});
