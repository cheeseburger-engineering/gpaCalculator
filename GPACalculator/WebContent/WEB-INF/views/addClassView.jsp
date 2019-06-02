<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c"%>
 
<!DOCTYPE html>
<html>

<head>
	<meta charset="UTF-8">
	<title>Add Class</title>
</head>

<body>
	
	<jsp:include page="_header.jsp"></jsp:include>
	<jsp:include page="_menu.jsp"></jsp:include>
	
	<h3>Add a class to recalculate your GPA</h3>
	
	<p style="color: red;">${errorString}</p>
	<form method="POST" action="${pageContext.request.contextPath}/addClass">
	<table>
		<tr>
			<td>Code</td>
			<td><input type="text" name="code" value="${product.code}" /></td>
		</tr>
           <tr>
           	<td>Name</td>
           	<td><input type="text" name="name" value="${product.name}" /></td>
           </tr>
           <tr>
           	<td>Price</td>
           	<td><input type="text" name="price" value="${product.price}" /></td>
           </tr>
           <tr>
           	<td colspan="2">
           		<input type="submit" value="Submit" />
           		<a href="classList">Cancel</a>
           	</td>
           </tr>
	</table>
	</form>

</body>
</html>