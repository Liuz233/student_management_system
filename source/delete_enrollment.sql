USE student_management_system;
DROP PROCEDURE IF EXISTS delete_enrollment; 
DELIMITER //
CREATE PROCEDURE delete_enrollment(
    IN p_student_id varchar(20),
    IN p_course_id varchar(20)
)
BEGIN
	DELETE FROM enrollments
    WHERE student_id=p_student_id AND course_id=p_course_id;
END //

DELIMITER ;