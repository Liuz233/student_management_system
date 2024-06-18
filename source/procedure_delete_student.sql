USE student_management_system;
Delimiter //
CREATE PROCEDURE delete_student_with_course(IN student_id varchar(20))
BEGIN
	DECLARE s1 INT DEFAULT 0;
    DECLARE s2 INT DEFAULT 0;
	DECLARE CONTINUE HANDLER FOR SQLEXCEPTION SET s1 = 1;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET s2 = 1;
    START TRANSACTION;
    -- 删除选课信息
    DELETE FROM enrollments WHERE enrollments.student_id = student_id;

    -- 删除学生信息
    DELETE FROM students WHERE students.student_id = student_id;
	IF s1 = 1 or s2 = 1 THEN 
		ROLLBACK;
	ELSE
		COMMIT;
	END IF;
END //
Delimiter ;