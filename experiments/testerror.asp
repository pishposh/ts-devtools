<%@ Language=VBScript %>
<%

sub KenFunc(x)
	Response.Write(1/x)
end sub

%>
<% %><!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8">
		<title></title>
	</head>
	<body>
<%
%><p>Err: <%=Err%>, <%=Err.Number%>, <%=Err.Description%></p><%

on error resume next
call KenFunc(0)

%><p>Err: <%=Err%>, <%=Err.Number%>, <%=Err.Description%></p><%

%>
		blah
	</body>
</html>