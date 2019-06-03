package org.cheeseburger.gpacalculator.servlet;
 
import java.io.IOException;
import java.sql.Connection;
import java.sql.SQLException;
 
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.cheeseburger.gpacalculator.beans.Grade;
import org.cheeseburger.gpacalculator.utils.DBUtils;
import org.cheeseburger.gpacalculator.utils.MyUtils;
 
@WebServlet(urlPatterns = { "/editClass" })
public class EditClassServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
 
    public EditClassServlet() {
        super();
    }
 
    // Show grade edit page.
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Connection conn = MyUtils.getStoredConnection(request);
 
        String code = (String) request.getParameter("code");
 
        Grade grade = null;
 
        String errorString = null;
 
        try {
            grade = DBUtils.findGrade(conn, code);
        } catch (SQLException e) {
            e.printStackTrace();
            errorString = e.getMessage();
        }
 
        // If no error.
        // The class does not exist to edit.
        // Redirect to classList page.
        if (errorString != null && grade == null) {
            response.sendRedirect(request.getServletPath() + "/classList");
            return;
        }
 
        // Store errorString in request attribute, before forward to views.
        request.setAttribute("errorString", errorString);
        request.setAttribute("grade", grade);
 
        RequestDispatcher dispatcher = request.getServletContext()
                .getRequestDispatcher("/WEB-INF/views/editClassView.jsp");
        dispatcher.forward(request, response);
 
    }
 
    // After the user modifies the product information, and click Submit.
    // This method will be executed.
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Connection conn = MyUtils.getStoredConnection(request);
 
        String code = (String) request.getParameter("code");
        String name = (String) request.getParameter("name");
        String gpaStr = (String) request.getParameter("gpa");
        float gpa = 0;
        try {
        	gpa = Float.parseFloat(gpaStr);
        } catch (Exception e) {
        }
        Grade grade = new Grade(code, name, gpa);
 
        String errorString = null;
 
        try {
            DBUtils.updateGrade(conn, grade);
        } catch (SQLException e) {
            e.printStackTrace();
            errorString = e.getMessage();
        }
        // Store information to request attribute, before forward to views.
        request.setAttribute("errorString", errorString);
        request.setAttribute("grade", grade);
 
        // If error, forward to Edit page.
        if (errorString != null) {
            RequestDispatcher dispatcher = request.getServletContext()
                    .getRequestDispatcher("/WEB-INF/views/editClassView.jsp");
            dispatcher.forward(request, response);
        }
        // If everything nice.
        // Redirect to the class listing page.
        else {
            response.sendRedirect(request.getContextPath() + "/classList");
        }
    }
 
}