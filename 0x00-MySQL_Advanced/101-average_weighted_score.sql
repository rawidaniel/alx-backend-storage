-- A SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN UPDATE users AS user,(
	SELECT user.id, SUM(score * weight) / SUM(weight) AS wt_avg
	FROM users AS user
	JOIN corrections AS corr 
	ON user.id = corr.user_id
	JOIN projects AS pro
	On corr.project_id = pro.id
	GROUP BY user.id) wt_all
  
	SET user.average_score = wt_all.wt_avg
	WHERE user.id = wt_all.id;
END $$
DELIMITER ;
