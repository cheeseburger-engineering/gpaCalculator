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
 
@WebServlet(urlPatterns = { "/addClass" })
public class AddClassServlet extends HttpServlet {
    private static final long serialVersionUID = 1L;
 
    public AddClassServlet() {
        super();
    }
 
    // Show product creation page.
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
 
        RequestDispatcher dispatcher = request.getServletContext()
                .getRequestDispatcher("/WEB-INF/views/addClassView.jsp");
        dispatcher.forward(request, response);
    }
 
    // When the user enters the product information, and click Submit.
    // This method will be called.
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        Connection conn = MyUtils.getStoredConnection(request);
 
        String code = (String) request.getParameter("code");
        String name = (String) request.getParameter("name");
        String priceStr = (String) request.getParameter("price");
        float price = 0;
        try {
            price = Float.parseFloat(priceStr);
        } catch (Exception e) {
        }
        Grade grade = new Grade(code, name, price);
 
        String errorString = null;
 
        // Product ID is the string literal [a-zA-Z_0-9]
        // with at least 1 character
        String regex = "\\w+";
 
        if (code == null || !code.matches(regex)) {
            errorString = "Product Code invalid!";
        }
 
        if (errorString == null) {
            try {
                DBUtils.insertGrade(conn, grade);
            } catch (SQLException e) {
                e.printStackTrace();
                errorString = e.getMessage();
            }
        }
 
        // Store infomation to request attribute, before forward to views.
        request.setAttribute("errorString", errorString);
        request.setAttribute("grade", grade);
 
        // If error, forward to Edit page.
        if (errorString != null) {
            RequestDispatcher dispatcher = request.getServletContext()
                    .getRequestDispatcher("/WEB-INF/views/addClassView.jsp");
            dispatcher.forward(request, response);
        }
        // If everything nice.
        // Redirect to the class listing page.
        else {
            response.sendRedirect(request.getContextPath() + "/classList");
        }
    }
 
}