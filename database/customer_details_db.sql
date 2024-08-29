CREATE DATABASE customer_details;

USE customer_details;

CREATE TABLE emails (
id INT NOT NULL auto_increment Primary Key,
first_name VARCHAR(50) NOT NULL, 
email_address VARCHAR(100) NOT NULL);


INSERT INTO emails (
id, first_name, email_address)
VALUES 
(1, "John", "john.smith@example.com"),
(2, "Jane", "jane.doe@example.com"),
(3, "Michael", "michael.johnson@example.com"),
(4, "Emily", "emily.davis@example.com"),
(5, "William", "william.brown@example.com"),
(6, "Linda", "linda.wilson@example.com"),
(7, "Robert", "robert.taylor@example.com"),
(8, "Patricia", "patricia.anderson@example.com"),
(9, "David", "david.thomas@example.com"),
(10, "Jennifer", "jennifer.moore@example.com"),
(11, "Charles", "charles.martin@example.com"),
(12, "Susan", "susan.jackson@example.com"),
(13, "Joseph", "joseph.white@example.com"),
(14, "Mary", "mary.harris@example.com"),
(15, "Christopher", "christopher.clark@example.com"),
(16, "Barbara", "barbara.lewis@example.com"),
(17, "Daniel", "daniel.walker@example.com"),
(18, "Jessica", "jessica.hall@example.com"),
(19, "Matthew", "matthew.young@example.com"),
(20, "Elizabeth", "elizabeth.king@example.com");
