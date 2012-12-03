#!/usr/bin/env node

/**
 *  Intended for use with /test/unload.html, unload_frame.html. Receives POSTed
 *  requests like { msg: "blah", delay_ms: 2000, payload: "..." }, logs to console
 *  and sends a response after delaying delay_ms. payload can be whatever.
 */

var http = require('http');
var qs = require('querystring');

var num_reqs = 0;

http.createServer(function (req, res) {
  var req_id = ++num_reqs;
  var body = "";
  
  console.log(req_id + ": request started");
  
  req.addListener("data", function(chunk) {
    body += chunk;
  });
  
  req.addListener("close", function() {
    console.log(req_id + ": request died after " + (body.length / (1024 * 1024)).toFixed(1) + " MB");
  });
  
  req.addListener("end", function() {
    req_obj = qs.parse(body);
    
    console.log(
      req_id + ": (\"" + req_obj.msg + "\") " + (body.length / (1024 * 1024)).toFixed(1)
      + " MB request received, delaying " + req_obj.delay_ms + " ms"
    );
    
    setTimeout(function() {
      res.writeHead(200, {
        "Content-Type": "text/plain",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, GET, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
        "Cache-Control": "no-cache"
      });
      res.end("delayed response\n");
      console.log(req_id + ": (\"" + req_obj.msg + "\") response sent");
      
    }, req_obj.delay_ms);
  });
}).listen(1337);
