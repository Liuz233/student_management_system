USE student_management_system;
DROP FUNCTION IF EXISTS calculate_weighted_gpa;
DELIMITER //
CREATE FUNCTION calculate_weighted_gpa(student_id varchar(20)) RETURNS FLOAT
DETERMINISTIC
BEGIN
    DECLARE total_credits FLOAT;
    DECLARE total_grade_points FLOAT;
	DECLARE grades FLOAT;
    DECLARE gpas FLOAT;
    
    SELECT SUM(credits) INTO total_credits
    FROM enrollments
    INNER JOIN courses ON enrollments.course_id = courses.course_id
    WHERE enrollments.student_id = student_id
    AND enrollments.grade IS NOT NULL;

    SELECT SUM(credits * grade) INTO total_grade_points
    FROM enrollments
    INNER JOIN courses ON enrollments.course_id = courses.course_id
    WHERE enrollments.student_id = student_id
    AND enrollments.grade IS NOT NULL;

    IF total_credits > 0 THEN
		SET grades = total_grade_points / total_credits;
    ELSE
		SET grades = 0.0;
    END IF;
     IF grades >= 95 THEN
        SET gpas = 4.3;
    ELSEIF grades >= 90 THEN
        SET gpas = 4.0;
    ELSEIF grades >= 85 THEN
        SET gpas = 3.7;
    ELSEIF grades >= 82 THEN
        SET gpas = 3.3;
    ELSEIF grades >= 78 THEN
        SET gpas = 3.0;
    ELSEIF grades >= 74 THEN
        SET gpas = 2.7;
    ELSEIF grades >= 72 THEN
        SET gpas = 2.3;
    ELSEIF grades >= 68 THEN
        SET gpas = 2.0;
    ELSEIF grades >= 65 THEN
        SET gpas = 1.7;
    ELSEIF grades >= 64 THEN
        SET gpas = 1.5;
    ELSEIF grades >= 61 THEN
        SET gpas = 1.3;
    ELSEIF grades >= 60 THEN
        SET gpas = 1.0;
    ELSE
        SET gpas = 0.0;
    END IF;
    RETURN gpas;
END //

DELIMITER ;
