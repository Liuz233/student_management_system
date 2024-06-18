USE student_management_system;
DROP PROCEDURE IF EXISTS edit_grade; 
DELIMITER //
CREATE PROCEDURE edit_grade(
    IN p_student_id varchar(20),
    IN p_course_id varchar(20),
    IN p_grade FLOAT
)
BEGIN
	UPDATE enrollments
    SET grade = p_grade
    WHERE student_id=p_student_id AND course_id=p_course_id;
END //

DELIMITER ;