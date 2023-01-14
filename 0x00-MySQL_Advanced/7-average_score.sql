-- A SQL script that creates a stored procedure ComputeAverageScoreForUser that computes and store the average score for a studet
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;
DELIMITER $$
CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections AS cor
        WHERE cor.user_id = user_id
    )
    WHERE id = user_id;
END $$
DELIMITER ;
