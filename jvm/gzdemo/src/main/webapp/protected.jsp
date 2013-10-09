<html>
<body>
<h2>Protected!</h2>
<h3>Eso es todo: FIN</h3>
<%
String username = request.getRemoteUser();
%>
<span>Hola <%= username %>.</span>
</body>
</html>
