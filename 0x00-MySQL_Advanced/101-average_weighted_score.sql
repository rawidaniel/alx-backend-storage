-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN DECLARE weight_average_score FLOAT;
    
    SET weight_average_score = (
	SELECT SUM(score * weight) / SUM(weight)
	FROM users AS user
	JOIN corrections AS corr 
	ON user.id = corr.user_id
	JOIN projects AS pro
	On corr.project_id = pro.id
    );
    UPDATE users
    SET average_score = weight_average_score;
END $$
DELIMITER ;
