<%@ page language="java" contentType="text/html; charset=UTF-8" pageEncoding="UTF-8"%>
    
<div style="padding: 5px;">
	
	<a href="${pageContext.request.contextPath}/">Home</a>
	|
	<a href="${pageContext.request.contextPath}/classList">Grade List</a>
	|
	<a href="${pageContext.request.contextPath}/accountInfo">Account Information</a>
	|
	<!-- Conditionally display Sign In or Sign Out -->
	<a href="${pageContext.request.contextPath}/login">
		<% if(org.cheeseburger.gpacalculator.utils.MyUtils.getLoginedUser(session) == null){ %>
			Login
		<% } else { %>
			Logout
		<% } %>
	</a>
    
</div>  