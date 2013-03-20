<%@ Language=VBScript %>
<% Option Explicit %>
<% 
	Response.CharSet = "utf-8"
	Response.CodePage = 65001
%>
<!--#INCLUDE FILE="./codepage-utf8-import.asp"-->
<%
	'Response.CodePage = 65001
%>
<% %><!DOCTYPE html>
<html>
<head>
	<title>VBScript CodePage Test</title>
</head>
<body>
	<p>
		Response.CharSet: <%=Server.HTMLEncode(Response.CharSet)%><br>
		Response.CodePage: <%=Server.HTMLEncode(Response.CodePage)%>
	</p>
	
	<p>
		Trademark: ™<br>
		Greek:       .<br>
		SIP: 
	</p>
	
	<p>
		<%=test_str%>
	</p>
	
	<p>
		<%=Replace(test_str, vbNewline, "<br>",1,-1,vbBinaryCompare)%>
	</p>
	
	<p>
		<%=Replace(test_str, vbNewline, "<br>",1,-1,vbTextCompare)%>
	</p>
	
	<p>
		<%=Server.HTMLEncode(test_str)%>
	</p>
</body>
</html>
