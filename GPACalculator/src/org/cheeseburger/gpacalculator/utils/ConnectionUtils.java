package org.cheeseburger.gpacalculator.utils;
 
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
 
public class ConnectionUtils {
 
    public static Connection getConnection() 
              throws ClassNotFoundException, SQLException {
 
        String hostName = "localhost";
        String sid = "xe";
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
     
    public static void closeQuietly(Connection conn) {
        try {
            conn.close();
        } catch (Exception e) {
        }
    }
 
    public static void rollbackQuietly(Connection conn) {
        try {
            conn.rollback();
        } catch (Exception e) {
        }
    }
    
}