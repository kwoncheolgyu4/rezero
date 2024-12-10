package org.zerock.persistence;

import static org.junit.Assert.fail;
import java.sql.Connection;
import java.sql.DriverManager;
import org.junit.Test;
import lombok.extern.log4j.Log4j;

public class JDBCTest {
	static {
		try {
			Class.forName("oracle.jdbc.driver.OracleDriver");
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	@Test	
	public void testConnection() {
		// 소괄호 안에 connection 을 해주면 자동으로 close.
		try (Connection con = DriverManager.getConnection("jdbc:oracle:thin:@192.168.0.86:1521:xe", "proj",
				"proj")) {
		} catch (Exception e) {
			fail(e.getMessage());
		}
	}
}