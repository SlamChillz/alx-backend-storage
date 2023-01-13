-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers
-- that computes and store the average weighted score for all students.
DROP PROCEDURE IF EXISTS `ComputeAverageWeightedScoreForUsers`;

DELIMITER |
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
	DECLARE userid, done INT;
	DECLARE weighted_average FLOAT;
	DECLARE cur CURSOR FOR
		SELECT user_id, SUM(score * weight) / SUM(weight)
		FROM corrections c
		LEFT JOIN projects p ON c.project_id = p.id
		GROUP BY user_id;
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN cur;

	insert_weighted_average:
	REPEAT
		FETCH cur INTO userid, weighted_average;
		UPDATE users SET average_score = weighted_average WHERE id = userid;
	UNTIL done = 1
	END REPEAT;

	CLOSE cur;
END;
|

DELIMITER ;
