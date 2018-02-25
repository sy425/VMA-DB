-- -----------------------------------------------------
-- LW:  Events to purge the database of
-- 		post procedure responses, appointments, and
--      patient records that are older than 2 weeks
-- -----------------------------------------------------

SET SQL_SAFE_UPDATES = 0;

CREATE EVENT IF NOT EXISTS vma.dailyPurge
    ON SCHEDULE EVERY 1 DAY
    COMMENT 'Purges records older than 2 weeks past the appointment date'
    DO
        DELETE FROM vma.postprocedurequestionresponse
        WHERE AppointmentID IN (
                SELECT AppointmentID
                FROM vma.appointment
                WHERE DATEDIFF(CURRENT_DATE, TimeDate) > 14
                )
            AND PostProcedureQuestionID IN (
                SELECT ppq.PostProcedureQuestionID
                FROM vma.postprocedurequestion ppq
                INNER JOIN vma.surveytype st
                    ON ppq.SurveyTypeID = st.SurveyTypeID
                    AND st.Category = 'Post Procedure'
            );

         DELETE FROM vma.appointment
                 WHERE DATEDIFF(CURRENT_DATE, TimeDate) > 14;

         DELETE FROM vma.patient
                 WHERE PatientID NOT IN (
                     SELECT PatientID
                     FROM vma.appointment
                 );

SET SQL_SAFE_UPDATES = 1;