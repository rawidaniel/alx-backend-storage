-- SQL script that creates a function SafeDiv that divides (and returns) the first by the second number or returns 0 if the second number is equal to 0
DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$
CREATE FUNCTION SafeDiv (firstnum INT,  secondnum INT)
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE output FLOAT DEFAULT 0;
    IF (secondnum <> 0) THEN
        SET output = firstnum / secondnum;
    END IF;
    RETURN output;
END $$
DELIMITER ;
