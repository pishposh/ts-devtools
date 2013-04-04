require.config({
  paths: { 
    "jquery": "lib/jquery-1.9.1"
  }
});

require(["TS", "jquery"], function(TS, $) {
  
  $(function(){
    $("body").prepend("<p>Hello from main.js, where TS.hello is " + TS.hello + "!</p>");
  });
  
});
