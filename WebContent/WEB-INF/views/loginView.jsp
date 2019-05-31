<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<!DOCTYPE html>
<html>

<head>
	<meta charset="UTF-8">
	<title>Login</title>
</head>

<body>

	<jsp:include page="_header.jsp"></jsp:include>
	<jsp:include page="_menu.jsp"></jsp:include>
	
	<h3>Please loging to view your saved classes</h3>
	
	<p style="color: red;">${errorString}</p>
	<form method="POST" action="${pageContext.request.contextPath}/login">
		<table>
			<tr>
				<td>User Name</td>
				<td><input type="text" name="userName" value= "${user.userName}" /> </td>
			</tr>
            <tr>
            	<td>Password</td>
            	<td><input type="text" name="password" value= "${user.password}" /> </td>
            </tr>
            <tr>
            	<td>Remember me</td>
            	<td><input type="checkbox" name="rememberMe" value= "Y" /> </td>
            </tr>
            <tr>
            	<td colspan ="2">
            		<input type="submit" value= "Submit" />
            		<a href="${pageContext.request.contextPath}/">Cancel</a>
            	</td>
            </tr>
		</table>
	</form>
 
</body>
</html>