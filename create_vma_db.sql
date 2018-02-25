-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
SHOW WARNINGS;
-- -----------------------------------------------------
-- Schema vma
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema vma
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `vma` DEFAULT CHARACTER SET utf8 ;
SHOW WARNINGS;
USE `vma` ;

-- -----------------------------------------------------
-- Table `vma`.`patient`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`patient` (
  `PatientID` INT(10) NOT NULL AUTO_INCREMENT,
  `PhoneNumber` INT(10) NOT NULL,
  `UniqueCode` CHAR(6) NOT NULL,
  `IsAuthenticated` TINYINT(1) NOT NULL,
  `PIN` INT(4) NULL DEFAULT NULL,
  `IsBloodThinner` TINYINT(1) NOT NULL,
  `IsNonSteroidal` TINYINT(1) NOT NULL,
  `IsAnesthesia` VARCHAR(500) NOT NULL,
  `IsIronSupplement` TINYINT(1) NOT NULL,
  `IsPulmonaryIssue` VARCHAR(500) NOT NULL,
  `IsAuthDefibrillator` TINYINT(1) NOT NULL,
  `IsAllergy` VARCHAR(500) NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`PatientID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;
CREATE UNIQUE INDEX `UniqueCode` ON `vma`.`patient` (`UniqueCode` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`medicalprocedure`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`medicalprocedure` (
  `MedicalProcedureID` INT(10) NOT NULL AUTO_INCREMENT,
  `ProcedureType` VARCHAR(30) NOT NULL,
  `ProcedureDetails` TEXT NOT NULL,
  `AssociatedSurveys` VARCHAR(100) NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`MedicalProcedureID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`appointment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`appointment` (
  `AppointmentID` INT(10) NOT NULL AUTO_INCREMENT,
  `PatientID` INT(10) NOT NULL,
  `MedicalProcedureID` INT(10) NOT NULL,
  `TimeDate` DATETIME NOT NULL,
  `LocationAddress` VARCHAR(100) NOT NULL,
  `LocationPhoneNumber` INT(10) NOT NULL,
  `Provider` VARCHAR(30) NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`AppointmentID`),
  CONSTRAINT `appointment_ibfk_1`
    FOREIGN KEY (`PatientID`)
    REFERENCES `vma`.`patient` (`PatientID`),
  CONSTRAINT `appointment_ibfk_2`
    FOREIGN KEY (`MedicalProcedureID`)
    REFERENCES `vma`.`medicalprocedure` (`MedicalProcedureID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;
CREATE INDEX `PatientID` ON `vma`.`appointment` (`PatientID` ASC);

SHOW WARNINGS;
CREATE INDEX `MedicalProcedureID` ON `vma`.`appointment` (`MedicalProcedureID` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`postprocedurequestion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`postprocedurequestion` (
  `PostProcedureQuestionID` INT(10) NOT NULL AUTO_INCREMENT,
  `SurveyType` VARCHAR(30) NOT NULL,
  `QuestionNumber` INT(5) NOT NULL,
  `QuestionDetails` TEXT NOT NULL,
  `AnswerOptions` JSON NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`PostProcedureQuestionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`postprocedurequestionresponse`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`postprocedurequestionresponse` (
  `PostProcedureQuestionResponseID` INT(10) NOT NULL AUTO_INCREMENT,
  `AppointmentID` INT(10) NOT NULL,
  `PostProcedureQuestionID` INT(10) NOT NULL,
  `Answer` TEXT NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`PostProcedureQuestionResponseID`),
  CONSTRAINT `postprocedurequestionresponse_ibfk_1`
    FOREIGN KEY (`AppointmentID`)
    REFERENCES `vma`.`appointment` (`AppointmentID`),
  CONSTRAINT `postprocedurequestionresponse_ibfk_2`
    FOREIGN KEY (`PostProcedureQuestionID`)
    REFERENCES `vma`.`postprocedurequestion` (`PostProcedureQuestionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;
CREATE INDEX `AppointmentID` ON `vma`.`postprocedurequestionresponse` (`AppointmentID` ASC);

SHOW WARNINGS;
CREATE INDEX `PostProcedureQuestionID` ON `vma`.`postprocedurequestionresponse` (`PostProcedureQuestionID` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`preprocedurequestion`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`preprocedurequestion` (
  `PreProcedureQuestionID` INT(10) NOT NULL AUTO_INCREMENT,
  `QuestionDetails` TEXT NOT NULL,
  `AnswerOptions` JSON NOT NULL,
  `AttributeName` VARCHAR(30) NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`PreProcedureQuestionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`preprocedurequestionnumber`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`preprocedurequestionnumber` (
  `PreProcedureQuestionNumberID` INT(10) NOT NULL AUTO_INCREMENT,
  `MedicalProcedureID` INT(10) NOT NULL,
  `PreProcedureQuestionID` INT(10) NOT NULL,
  `QuestionNumber` INT(5) NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`PreProcedureQuestionNumberID`),
  CONSTRAINT `preprocedurequestionnumber_ibfk_1`
    FOREIGN KEY (`MedicalProcedureID`)
    REFERENCES `vma`.`medicalprocedure` (`MedicalProcedureID`),
  CONSTRAINT `preprocedurequestionnumber_ibfk_2`
    FOREIGN KEY (`PreProcedureQuestionID`)
    REFERENCES `vma`.`preprocedurequestion` (`PreProcedureQuestionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;
CREATE INDEX `MedicalProcedureID` ON `vma`.`preprocedurequestionnumber` (`MedicalProcedureID` ASC);

SHOW WARNINGS;
CREATE INDEX `PreProcedureQuestionID` ON `vma`.`preprocedurequestionnumber` (`PreProcedureQuestionID` ASC);

SHOW WARNINGS;

-- -----------------------------------------------------
-- Table `vma`.`specialinstruction`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `vma`.`specialinstruction` (
  `SpecialInstructionID` INT(10) NOT NULL AUTO_INCREMENT,
  `AttributeName` VARCHAR(30) NOT NULL,
  `Instructions` TEXT NOT NULL,
  `CreateTS` DATETIME NOT NULL,
  PRIMARY KEY (`SpecialInstructionID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8;

SHOW WARNINGS;
CREATE UNIQUE INDEX `AttributeName` ON `vma`.`specialinstruction` (`AttributeName` ASC);

SHOW WARNINGS;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
