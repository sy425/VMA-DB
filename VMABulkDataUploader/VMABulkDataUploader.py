import sys
import Config
import csv
import os
import MySQLdb

TABLES = ["patient",
          "medicalprocedure",
          "appointment",
          "postprocedurequestion",
          "postprocedurequestionresponse",
          "preprocedurequestion",
          "preprocedurequestionnumber",
          "specialinstruction"]

TABLE_ATTRIBUTES = {}
TABLE_ATTRIBUTES["patient"] = ["PatientID",
                               "PhoneNumber",
                               "UniqueCode",
                               "IsAuthenticated",
                               "PIN",
                               "IsBloodThinner",
                               "IsNonSteroidal",
                               "IsAnesthesia",
                               "IsIronSupplement",
                               "IsPulmonaryIssue",
                               "IsAuthDefibrillator",
                               "IsAllergy"]
TABLE_ATTRIBUTES["medicalprocedure"] = ["MedicalProcedureID",
                                        "ProcedureType",
                                        "ProcedureDetails",
                                        "AssociatedSurveys"]
TABLE_ATTRIBUTES["appointment"] = ["AppointmentID",
                                   "PatientID",
                                   "MedicalProcedureID",
                                   "TimeDate",
                                   "LocationAddress",
                                   "LocationPhoneNumber",
                                   "Provider"]
TABLE_ATTRIBUTES["postprocedurequestion"] = ["PostProcedureQuestionID",
                                             "SurveyType",
                                             "QuestionNumber",
                                             "QuestionDetails",
                                             "AnswerOptions"]
TABLE_ATTRIBUTES["postprocedurequestionresponse"] = ["PostProcedureQuestionResponseID",
                                                     "AppointmentID",
                                                     "PostProcedureQuestionID",
                                                     "Answer"]
TABLE_ATTRIBUTES["preprocedurequestion"] = ["PreProcedureQuestionID",
                                            "QuestionDetails",
                                            "AnswerOptions",
                                            "AttributeName"]
TABLE_ATTRIBUTES["preprocedurequestionnumber"] = ["PreProcedureQuestionNumberID",
                                                  "MedicalProcedureID",
                                                  "PreProcedureQuestionID",
                                                  "QuestionNumber"]
TABLE_ATTRIBUTES["specialinstruction"] = ["SpecialInstructionID",
                                          "AttributeName",
                                          "Instructions"]

valid_files = {}

# DK: Connection to data using Config.py file
def connectToDatabase():
    database = MySQLdb.connect(Config.HOST,
                               Config.USER,
                               Config.PASSWORD,
                               Config.DATABASE_NAME)

    return database

# DK: Validates that supplied CSV files have the same name and attributes
#     with their respective table and imports their data
def validateCSVFile(file):
    validated_attributes = True
    row_count = 0
    table_contents = []
    # Get the filename minus the extension
    table_name = os.path.splitext(file)[0].lower()

    # If the filename matches a table in the database, continue
    if (table_name in TABLES):
        with open(file) as table_csv:
            read_table_csv = csv.reader(table_csv, delimiter=',')

            # Loop through each row in the CSV and validate the header
            for row in read_table_csv:
                if (validated_attributes) :
                    # If the given row matches the number of attributes for a given table, continue
                    if (len(row) == len(TABLE_ATTRIBUTES[table_name])) :
                        # Validate header row
                        if (row_count == 0):
                            for i in range(0,len(row)) :
                                if (str(row[i]).lower() != str(TABLE_ATTRIBUTES[table_name][i]).lower()):
                                    print( "Attributes for {0} do not match with the {1} table. Skipping...".format(file , table_name) )
                                    validated_attributes = False
                                    break
                        # Append row of data
                        else:
                            table_contents.append(row)
                        row_count += 1
                    # Failure of attribute validation due to improper number of attributes
                    elif (len(row) != len(TABLE_ATTRIBUTES[table_name]) and row_count == 0):
                        validated_attributes = False
                        break
                # If header row validation fails, break the loop
                elif (not validated_attributes):
                    break
            # If valid data was contained in the CSV file, add it to the dictionary of valid file contents
            if ( len(table_contents) > 0 ) :
                valid_files[table_name] = table_contents
    else:
        print( "{0} is not named after a table in the VMA database. Skipping...".format( file ) )

    # DK: Attempt to upload all found, valid data to the database
def uploadAllTableData(database, cursor):
    sql_statements = ""
    sql_statements += uploadPatientTableData(database, cursor)
    sql_statements += uploadMedicalProcedureTableData(database, cursor)
    sql_statements += uploadAppointmentTableData(database, cursor)
    sql_statements += uploadPostProcedureQuestionTableData(database, cursor)
    sql_statements += uploadPostProcedureQuestionResponseTableData(database, cursor)
    sql_statements += uploadPreProcedureQuestionTableData(database, cursor)
    sql_statements += uploadPreProcedureQuestionNumberTableData(database, cursor)
    sql_statements += uploadSpecialInstructionTableData(database, cursor)

    return sql_statements

# DK: Upload all valid patient table data
def uploadPatientTableData(database, cursor):
    sql_statements = ""
    if ( "patient" in valid_files.keys() ):
        for row in valid_files["patient"]:
            sql_statements += uploadRowToPatientTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid medicalprocedure table data
def uploadMedicalProcedureTableData(database, cursor):
    sql_statements = ""
    if ( "medicalprocedure" in valid_files.keys() ):
        for row in valid_files["medicalprocedure"]:
            sql_statements += uploadRowToMedicalProcedureTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid appointment table data
def uploadAppointmentTableData(database, cursor):
    sql_statements = ""
    if ( "appointment" in valid_files.keys() ):
        for row in valid_files["appointment"]:
            sql_statements += uploadRowToAppointmentTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid postprocedurequestion table data
def uploadPostProcedureQuestionTableData(database, cursor):
    sql_statements = ""
    if ( "postprocedurequestion" in valid_files.keys() ):
        for row in valid_files["postprocedurequestion"]:
            sql_statements += uploadRowToPostProcedureQuestionTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid postprocedurequestionresponse table data
def uploadPostProcedureQuestionResponseTableData(database, cursor):
    sql_statements = ""
    if ( "postprocedurequestionresponse" in valid_files.keys() ):
        for row in valid_files["postprocedurequestionresponse"]:
            sql_statements += uploadRowToPostProcedureQuestionResponseTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid preprocedurequestion table data
def uploadPreProcedureQuestionTableData(database, cursor):
    sql_statements = ""
    if ( "preprocedurequestion" in valid_files.keys() ):
        for row in valid_files["preprocedurequestion"]:
            sql_statements += uploadRowToPreProcedureQuestionTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid preprocedurequestionnumber table data
def uploadPreProcedureQuestionNumberTableData(database, cursor):
    sql_statements = ""
    if ( "preprocedurequestionnumber" in valid_files.keys() ):
        for row in valid_files["preprocedurequestionnumber"]:
            sql_statements += uploadRowToPreProcedureQuestionNumberTable(database, cursor, row)

    return sql_statements

# DK: Upload all valid specialinstruction table data
def uploadSpecialInstructionTableData(database, cursor):
    sql_statements = ""
    if ( "specialinstruction" in valid_files.keys() ):
        for row in valid_files["specialinstruction"]:
            sql_statements += uploadRowToSpecialInstructionTable(database, cursor, row)

    return sql_statements

# DK: Uploads a single row of valid data to the patient table
def uploadRowToPatientTable(database, cursor, row):
    sql_insert = ""
    if ( len(row) == len(TABLE_ATTRIBUTES["patient"]) ):
        sql_insert = "INSERT INTO patient(PatientID,PhoneNumber,UniqueCode," \
                     "IsAuthenticated,PIN,IsBloodThinner,IsNonSteroidal,IsAnesthesia," \
                     "IsIronSupplement,IsPulmonaryIssue,IsAuthDefibrillator,IsAllergy) " \
                     "VALUES ({0},{1},\"{2}\",{3},{4},{5},{6},\"{7}\",{8},\"{9}\",{10},\"{11}\");".format(row[0],
                                                                                                          row[1],
                                                                                                          row[2],
                                                                                                          row[3],
                                                                                                          row[4],
                                                                                                          row[5],
                                                                                                          row[6],
                                                                                                          row[7],
                                                                                                          row[8],
                                                                                                          row[9],
                                                                                                          row[10],
                                                                                                          row[11])
        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the medicalprocedure table
def uploadRowToMedicalProcedureTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["medicalprocedure"])):
        sql_insert =  "INSERT INTO medicalprocedure(MedicalProcedureID,ProcedureType,ProcedureDetails,AssociatedSurveys) " \
                      "VALUES ({0},\"{1}\",\"{2}\",\"{3}\");".format(row[0],row[1],row[2],row[3])
        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the appointment table
def uploadRowToAppointmentTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["appointment"])):
        sql_insert = "INSERT INTO appointment(AppointmentID,PatientID,MedicalProcedureID,TimeDate,LocationAddress," \
                     "LocationPhoneNumber,Provider) VALUES ({0},{1},{2},\'{3}\',\"{4}\",{5},\"{6}\");".format(row[0],
                                                                                                             row[1],
                                                                                                             row[2],
                                                                                                             row[3],
                                                                                                             row[4],
                                                                                                             row[5],
                                                                                                             row[6])

        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the postprocedurequestion table
def uploadRowToPostProcedureQuestionTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["postprocedurequestion"])):
        sql_insert = "INSERT INTO postprocedurequestion(PostProcedureQuestionID,SurveyType,QuestionNumber,QuestionDetails,AnswerOptions) " \
                     "VALUES ({0},\"{1}\",{2},\"{3}\",\'{4}\');".format(row[0],row[1],row[2],row[3],row[4].strip("\n"))
        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the postprocedurequestionresponse table
def uploadRowToPostProcedureQuestionResponseTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["postprocedurequestionresponse"])):
        sql_insert = "INSERT INTO postprocedurequestionresponse(PostProcedureQuestionResponseID,AppointmentID,PostProcedureQuestionID,Answer) " \
                     "VALUES ({0},{1},{2},\"{3}\");".format(row[0],row[1],row[2],row[3])

        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the preprocedurequestion table
def uploadRowToPreProcedureQuestionTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["preprocedurequestion"])):
        sql_insert = "INSERT INTO preprocedurequestion(PreProcedureQuestionID,QuestionDetails,AnswerOptions,AttributeName) " \
                     "VALUES ({0},\"{1}\",\'{2}\',\"{3}\");".format(row[0],row[1],row[2],row[3])

        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the preprocedurequestionnumber table
def uploadRowToPreProcedureQuestionNumberTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["preprocedurequestionnumber"])):
        sql_insert = "INSERT INTO preprocedurequestionnumber(PreProcedureQuestionNumberID,MedicalProcedureID,PreProcedureQuestionID,QuestionNumber) " \
                     "VALUES ({0},{1},{2},{3});".format(row[0],row[1],row[2],row[3])

        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Uploads a single row of valid data to the specialinstruction table
def uploadRowToSpecialInstructionTable(database, cursor, row):
    sql_insert = ""
    if (len(row) == len(TABLE_ATTRIBUTES["specialinstruction"])):
        sql_insert = "INSERT INTO specialinstruction(SpecialInstructionID,AttributeName,Instructions) " \
                     "VALUES ({0},\"{1}\",\"{2}\");".format(row[0],row[1],row[2])

        try:
            cursor.execute(sql_insert)
            database.commit()
        except:
            database.rollback()

    return sql_insert + "\n"

# DK: Deletes all data from all tables in the database
def deleteAllDataFromDatabase(database, cursor):
    try:
        cursor.execute("TRUNCATE TABLE specialinstruction;")
        cursor.execute("TRUNCATE TABLE postprocedurequestionresponse;")
        cursor.execute("TRUNCATE TABLE preprocedurequestionnumber;")
        cursor.execute("DELETE FROM postprocedurequestion;")
        cursor.execute("DELETE FROM preprocedurequestion;")
        cursor.execute("DELETE FROM appointment;")
        cursor.execute("DELETE FROM medicalprocedure;")
        cursor.execute("DELETE FROM patient;")
        database.commit()
    except:
        database.rollback()

# DK: simple output to a file (overwrites the specified file if it exists)
def outputToFile(filename, data):
    with open(filename,"w+") as file:
        file.write(data)
        file.close()

def main(argv):
    # If no arguments are given, exit...
    if (len(argv) < 1) :
        exit(1)

    # Validate each specified file and get all of their contents in the global dictionary
    for file in argv :
        validateCSVFile(file)

    # Connect to the database and initialize a cursor object
    database = connectToDatabase()
    cursor = database.cursor()

    # Purge all data from all tables (if specified in Config.py)
    if (Config.PURGE_TABLE_DATA_BEFORE_UPLOAD):
        deleteAllDataFromDatabase(database,cursor)

    # Upload all valid data from the specified CSV files
    sql_statements = uploadAllTableData(database, cursor)

    # Output a SQL script of all insertion calls
    outputToFile("output.sql", sql_statements)

    database.close()

if __name__ == "__main__":
    main(sys.argv[1:])