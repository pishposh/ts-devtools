<%@ Language=VBScript %>
<%  option explicit
	' no codepage, no bom, no nothing
%>
<% %><!DOCTYPE html>
<head>
	<meta charset="utf-8">
	<title>Horror Lab Form Submission</title>
	<style type="text/css">
	
body {
	background: -webkit-gradient(radial, center center, 0, center center, 417, color-stop(0, #eee), color-stop(1, #ddd)) fixed;
	background: -webkit-radial-gradient(center, circle cover, #eee 0%, #ddd 100%) fixed;
	background: -moz-radial-gradient(center, circle farthest-corner, #eee 0%, #ddd 100%) fixed;
	background: -ms-radial-gradient(center, circle farthest-corner, #eee 0%, #ddd 100%) fixed;
	text-align: center; font-family: calibri;
}

h1 { text-transform: uppercase }

	</style>
	<script src="http://code.jquery.com/jquery.min.js"></script>
</head>
 
<body>
 
<h1>Submit!</h1>

<p><% Response.Write(Request.Form.Count()) %> items in Request.Form array</p>

<p>
<%
dim i
for i = 1 to Request.Form.count() 
    Response.Write(Server.HTMLEncode(Request.Form.key(i)) & "(" & i & ")" & " = ") 
    Response.Write(Server.HTMLEncode(Request.Form.item(i)) & "<br>") 
next
%>
</p>

</body>
</html>