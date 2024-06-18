USE student_management_system;
Delimiter //
CREATE PROCEDURE delete_course_with_student(IN course_id varchar(20))
BEGIN
	DECLARE s1 INT DEFAULT 0;
    DECLARE s2 INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s1 = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET s2 = 1;
    START TRANSACTION;
    -- 删除选课信息
    DELETE FROM enrollments WHERE enrollments.course_id = course_id;

    -- 删除学生信息
    DELETE FROM courses WHERE courses.course_id = course_id;
	IF s1 = 1 or s2 = 1 THEN 
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
END //
Delimiter ;