USE student_management_system;
DROP TRIGGER IF EXISTS calculate_gpa2;
DELIMITER //
CREATE TRIGGER calculate_gpa2 BEFORE INSERT ON enrollments FOR EACH ROW
BEGIN
    DECLARE grades float;
	DECLARE gpas float;
    SET grades = NEW.grade;


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

    -- 更新插入记录的绩点字段
    SET NEW.gpa = gpas;
END //

DELIMITER ;