<%@ page language="java" contentType="text/html; charset=UTF-8"
 pageEncoding="UTF-8"%>
<%@ taglib uri="http://java.sun.com/jsp/jstl/core" prefix="c" %>  
<!DOCTYPE html>
<html>
 <head>
    <meta charset="UTF-8">
    <title>Class and Grade List</title>
 </head>
 <body>
 
    <jsp:include page="_header.jsp"></jsp:include>
    <jsp:include page="_menu.jsp"></jsp:include>
 
    <h3>Class and Grade List</h3>
 
    <p style="color: red;">${errorString}</p>
 
    <table border="1" style="cellpadding:5" style="cellspacing:1" >
       <tr>
          <th>Code</th>
          <th>Class Name</th>
          <th>Grade (on 4.0 scale)</th>
          <th>Edit</th>
          <th>Delete</th>
       </tr>
       <c:forEach items="${gradeList}" var="grade" >
          <tr>
             <td>${grade.code}</td>
             <td>${grade.name}</td>
             <td>${grade.gpa}</td>
             <td>
                <a href="editClass?code=${grade.code}">Edit</a>
             </td>
             <td>
                <a href="deleteClass?code=${grade.code}">Delete</a>
             </td>
          </tr>
       </c:forEach>
    </table>
 
    <a href="addClass">Add a class and grade</a>
 
 </body>
</html>