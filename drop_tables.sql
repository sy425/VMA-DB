-- -----------------------------------------------------
-- LW: Drop all tables
--      This script is used when the DB must be reloaded
-- -----------------------------------------------------

SET FOREIGN_KEY_CHECKS=0;
SET UNIQUE_CHECKS=0;

DROP TABLE IF EXISTS `vma`.`patient`;
DROP TABLE IF EXISTS `vma`.`medicalprocedure`;
DROP TABLE IF EXISTS `vma`.`appointment`;
DROP TABLE IF EXISTS `vma`.`surveytype`;
DROP TABLE IF EXISTS `vma`.`postprocedurequestion`;
DROP TABLE IF EXISTS `vma`.`postprocedurequestionresponse`;
DROP TABLE IF EXISTS `vma`.`preprocedurequestion`;
DROP TABLE IF EXISTS `vma`.`preprocedurequestionnumber`;
DROP TABLE IF EXISTS `vma`.`specialinstruction`;

SET FOREIGN_KEY_CHECKS=1;
SET UNIQUE_CHECKS=1;