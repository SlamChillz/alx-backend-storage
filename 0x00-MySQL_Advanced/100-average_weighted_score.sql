-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser
-- that computes and store the average weighted score for a student.
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUser`;

DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN userid INT)
BEGIN
	UPDATE users SET average_score = (
		SELECT SUM(score * weight) / SUM(weight)
		FROM corrections c
		LEFT JOIN projects p ON c.project_id = p.id
		WHERE user_id = userid
	) WHERE id = userid;
END;
|

DELIMITER ;
