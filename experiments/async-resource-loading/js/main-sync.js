// wherein we pray we've remembered to load both jquery and TS

$(function(){
  $("#dynamic-content").append("<p>Hello from main.js, where TS.hello is " + TS.hello + "!</p>");
});
