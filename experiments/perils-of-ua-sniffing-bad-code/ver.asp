<%@ Language=VBScript %>
<% option explicit %>
<%

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' VBSCRIPT '''
'''                                                                                            '''


' getVersion: uaSearchString = e.g. "Firefox/" or "MSIE "
function getVersion(uaSearchString)
	dim re: set re = new RegExp
	re.Pattern = "\b"&uaSearchString&"([^\s]*)"
	
	dim matches: set matches = re.Execute(HTTP_USER_AGENT)
	if matches.Count > 0 then
		getVersion = matches(0).SubMatches(0)
	else
		getVersion = ""
	end if
	
	set matches = nothing
	set re = nothing
end function


' cmpVersions: returns negative if A < B, zero if A == B, positive if A > B
' note: only the leading numeric portion of each token is considered, so
' e.g. "1.2.3" == "1^999.2x8$&*@#&73462#@.3d4"; also, 0's are considered
' equivalent to empty string or nonexistent tokens, and leading zeros are
' discarded such that 3.0001 is considered the same as 3.1
function cmpVersions(verStrA, verStrB)
	if IsEmpty(verStrA) or IsNull(verStrA) then verStrA = ""
	if IsEmpty(verStrB) or IsNull(verStrB) then verStrB = ""
	dim vA: vA = Split(verStrA,".")
	dim vB: vB = Split(verStrB,".")
	dim uboundA: uboundA = UBound(vA)
	dim uboundB: uboundB = UBound(vB)
	dim i, L: if uboundA > uboundB then L = uboundA else L = uboundB
	for i = 0 to L
		dim a: if i <= uboundA then a = parseIntSafe(vA(i)) else a = 0
		dim b: if i <= uboundB then b = parseIntSafe(vB(i)) else b = 0
		if (a < b) then
			cmpVersions = -1
			exit function
		elseif (a > b) then
			cmpVersions = 1
			exit function
		end if
	next 'i
	cmpVersions = 0
end function


' majorVersionInt: "5c.842" => 5, "2e35" => 2, ".428" => 0
function majorVersionInt(verStr)
	majorVersionInt = versionInt(verStr, 0)
end function

' minorVersionInt: "2.24a18" => 24, "2e35.f" => 0, "1.050" => 50
function minorVersionInt(verStr)
	minorVersionInt = versionInt(verStr, 1)
end function

function versionInt(verStr, tokenIndex)
	if IsEmpty(verStr) or IsNull(verStr) then verStr = ""
	if IsEmpty(tokenIndex) or IsNull(tokenIndex) then tokenIndex = 0
	dim ver: ver = Split(verStr,".")
	if UBound(ver) >= tokenIndex then
		versionInt = parseIntSafe(ver(tokenIndex))
	else
		versionInt = 0
	end if
end function

' numericVersion: "2.24a18" => 2.24, "2e42.5" => 2.0, "1.50" => 1.5, "1.05" => 1.05
function numericVersion(verStr)
	if IsEmpty(verStr) or IsNull(verStr) then verStr = ""
	
	dim re: set re = new RegExp
	re.Pattern = "^\d*\.?\d*"
	dim matches: set matches = re.Execute(verStr)
	
	if IsNumeric(matches(0).Value) then
		numericVersion = CDbl(matches(0))
	else
		numericVersion = 0.0
	end if
	
	set matches = nothing
	set re = nothing
end function

function parseIntSafe(str)
	' returns 0 if unparsable
	dim re: set re = new RegExp
	re.Pattern = "^\d+"
	dim matches: set matches = re.Execute(str)
	if matches.Count > 0 then
		if IsNumeric(matches(0).Value) then
			parseIntSafe = CInt(matches(0).Value)
		else
			parseIntSafe = 0
		end if
	else
		parseIntSafe = 0
	end if
	
	set matches = nothing
	set re = nothing
end function


'''                                                                                            '''
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''' END VBSCRIPT '''


%>
<%%><!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>version parsing test</title>
<script>
/********************************************************************************* JAVASCRIPT ***/
/***                                                                                          ***/

// uaSearchString = e.g. "Firefox/" or "MSIE "
function getVersion(uaSearchString) {
	var matches = navigator.userAgent.match("\\b"+uaSearchString+"([^s]*)");
	return matches ? matches[1] : "";
}

// cmpVersions: returns negative if A < B, zero if A == B, positive if A > B
// note: only the leading numeric portion of each token is considered, so
// e.g. "1.2.3" == "1^999.2x8$&*@#&73462#@.3d4"; also, 0's are considered
// equivalent to empty string or nonexistent tokens, and leading zeros are
// discarded such that 3.0001 is considered the same as 3.1
function cmpVersions(verStrA, verStrB) {
	var vA = (verStrA || "").toString().split("."),
		vB = (verStrB || "").toString().split("."),
		i, L = vA.length > vB.length ? vA.length : vB.length;
	for (i = 0; i < L; i++) {
		var a = parseInt(vA[i], 10) || 0;
		var b = parseInt(vB[i], 10) || 0;
		if (a < b) { return -1; }
		if (a > b) { return +1; }
	}
	return 0;
}

// majorVersionInt: "5c.842" => 5, "2e35" => 2, ".428" => 0
function majorVersionInt(verStr) {
	return versionInt(verStr, 0)
}

// minorVersionInt: "2.24a18" => 24, "2e35.f" => 0, "1.050" => 50
function minorVersionInt(verStr) {
	return versionInt(verStr, 1)
}

function versionInt(verStr, tokenIndex) {
	return parseInt((verStr || "").toString().split(".")[tokenIndex || 0], 10) || 0;
}

// numericVersion: "2.24a18" => 2.24, "2e42.5" => 2.0, "1.50" => 1.5, "1.05" => 1.05
function numericVersion(verStr) {
	return parseFloat((verStr || "").match(/^\d*\.?\d*/)[0]) || 0.0;
}

/***                                                                                          ***/
/***************************************************************************** END JAVASCRIPT ***/

</script>
<style>
.x { display: inline-block; width: 2em; }
</style>
</head>
<body>

<%

call test("3.0001j28.005.00b49..0q.q0", "3.0001.005")
call test("1.010", "1.01")
call test("3.0001", "3.1")
call test("3.0.0.0", "3.1")
call test("3.10", "3.1")
call test("3", "3.0.0.0")
call test("3.0.0.2", "3.0.0.10")
call test("7","8")
call test("3b4.0au88&..^^U", "3.0.0.10")
call test("&U2x...x-42", "3.0.0.10")
call test("3-5.0.0.2", "3.0.0.10")
call test("3xdjk8.x*&^*^@^0.", "3.0.0.10")
call test("3b4.0au88&..^^U", "3.0.0.10")
call test("&U2x...x-42", "3.0.0.10")
call test("3-5.0.0.2", "3.0.0.10")
call test("3xdjk8.x*&^*^@^0.", "3.0.0.10")
call test("23846.p86y8yu*Y^EU*UI","jkqxjkqx")
call test("3@#^Y@#Y","425")
call test("24.7y7Y8.y","24")
call test(".","")
call test("","")
call test("","")
call test("","")
call test("","")
call test("","")
call test("","")
call test("","")
call test("","")

sub test(a,b)
	%>
<p>
	<span class="x">VB:</span> cmpVersions("<%=a%>","<%=b%>"): <%=cmpVersions(a,b)%><br>
	<span class="x">JS:</span> cmpVersions("<%=a%>","<%=b%>"): <script>document.write(cmpVersions("<%=a%>","<%=b%>"))</script>
</p>
<p>
	<span class="x">VB:</span> majorVersionInt("<%=a%>"): <%=majorVersionInt(a)%><br>
	<span class="x">JS:</span> majorVersionInt("<%=a%>"): <script>document.write(majorVersionInt("<%=a%>"))</script>
</p>
<p>
	<span class="x">VB:</span> minorVersionInt("<%=a%>"): <%=minorVersionInt(a)%><br>
	<span class="x">JS:</span> minorVersionInt("<%=a%>"): <script>document.write(minorVersionInt("<%=a%>"))</script>
</p>
<p>
	<span class="x">VB:</span> numericVersion("<%=a%>"): <%=numericVersion(a)%><br>
	<span class="x">JS:</span> numericVersion("<%=a%>"): <script>document.write(numericVersion("<%=a%>"))</script>
</p>
	<%
end sub

%>

</body>
</html>
