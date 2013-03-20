<%@ Language=VBScript CodePage=65001 %>
<% Option Explicit %>
<%
	Response.CodePage = 65001
	Response.Charset = "utf-8"
	
	dim test_str
	
	test_str = _
		"French: Il y a deux manières d’être malheureux: ou désirer ce que l’on n’a pas, ou posséder ce que l’on désirait."& vbNewline & _
		"Greek: Ἰοὺ ἰού· τὰ πάντʼ ἂν ἐξήκοι σαφῆ."& vbNewline & _
		"SIP: 𠜎𠜱𠝹𠱓𠱸𠲖𠳏𠳕𠴕𠵼𠵿𠸎𠸏𠹷𠺝𠺢𠻗𠻹𠻺𠼭𠼮𠽌𠾴𠾼𠿪𡁜𡁯𡁵𡁶𡁻𡃁𡃉𡇙𢃇𢞵𢫕𢭃𢯊𢱑𢱕𢳂𢴈𢵌𢵧𢺳𣲷𤓓𤶸𤷪𥄫𦉘𦟌𦧲𦧺𧨾𨅝𨈇𨋢𨳊𨳍𨳒𩶘"
%>
<% %><!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>VBScript CodePage Test</title>
</head>
<body>
	<p>
		<b>Response.Charset:</b> <%=Server.HTMLEncode(Response.CharSet)%><br>
		<b>Response.CodePage:</b> <%=Server.HTMLEncode(Response.CodePage)%>
	</p>
	
	<p>
		French: Il y a deux manières d’être malheureux: ou désirer ce que l’on n’a pas, ou posséder ce que l’on désirait.<br>
		Greek: Ἰοὺ ἰού· τὰ πάντʼ ἂν ἐξήκοι σαφῆ.<br>
		SIP: 𠜎𠜱𠝹𠱓𠱸𠲖𠳏𠳕𠴕𠵼𠵿𠸎𠸏𠹷𠺝𠺢𠻗𠻹𠻺𠼭𠼮𠽌𠾴𠾼𠿪𡁜𡁯𡁵𡁶𡁻𡃁𡃉𡇙𢃇𢞵𢫕𢭃𢯊𢱑𢱕𢳂𢴈𢵌𢵧𢺳𣲷𤓓𤶸𤷪𥄫𦉘𦟌𦧲𦧺𧨾𨅝𨈇𨋢𨳊𨳍𨳒𩶘
	</p>
	
	<p>
		<b>test_str</b><br>
		<%=test_str%>
	</p>
	
	<p>
		<b>Replace(test_str, vbNewline, "&lt;br&gt;",1,-1,vbBinaryCompare)</b><br>
		<%=Replace(test_str, vbNewline, "<br>",1,-1,vbBinaryCompare)%>
	</p>
	
	<p>
		<b>Replace(test_str, vbNewline, "&lt;br&gt;",1,-1,vbTextCompare)</b><br>
		<%=Replace(test_str, vbNewline, "<br>",1,-1,vbTextCompare)%>
	</p>
	
	<p>
		<b>Replace(Server.HTMLEncode(test_str), vbNewline, "&lt;br&gt;",1,-1,vbTextCompare)</b><br>
		<%=Replace(Server.HTMLEncode(test_str), vbNewline, "<br>",1,-1,vbTextCompare)%>
	</p>
</body>
</html>
