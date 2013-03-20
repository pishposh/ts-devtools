<%@ Language=VBScript %>
<% Option Explicit %>
<%
	dim test_str
	
	test_str = _
		"Trademark: ™"& vbNewline & _
		"Greek:       ."& vbNewline & _
		"SIP: "
%>

<% %><!DOCTYPE html>
<html>
<head>
	<title>VBScript CodePage Test</title>
</head>
<body>
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
