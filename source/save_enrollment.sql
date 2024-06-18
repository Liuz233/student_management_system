USE student_management_system;
DROP PROCEDURE IF EXISTS insert_enrollment; 
DELIMITER //
CREATE PROCEDURE insert_enrollment(
    IN p_student_id varchar(20),
    IN p_course_id varchar(20),
    IN p_grade FLOAT
)
BEGIN
    INSERT INTO enrollments (student_id, course_id, grade)
    VALUES (p_student_id, p_course_id, p_grade);
END //

DELIMITER ;