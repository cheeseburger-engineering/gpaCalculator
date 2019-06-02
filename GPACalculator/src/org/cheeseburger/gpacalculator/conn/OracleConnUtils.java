package org.cheeseburger.gpacalculator.conn;
 
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Statement;
  
public class OracleConnUtils {
  
   public static Connection getOracleConnection()
           throws ClassNotFoundException, SQLException {
        
       // Note: Change the connection parameters accordingly.
       String hostName = "localhost";
       String sid = "127";
       String userName = "gpauser";
       String password = "gpapass";
  
       return getOracleConnection(hostName, sid, userName, password);
   }
  
   public static Connection getOracleConnection(String hostName, String sid,
           String userName, String password) throws ClassNotFoundException,
           SQLException {
   
       Class.forName("oracle.jdbc.driver.OracleDriver");
  
       String connURL = "jdbc:oracle:thin:@" + hostName + ":1521:" + sid;
  
       Connection conn = DriverManager.getConnection(connURL, userName, password);
       return conn;
   }
   
}