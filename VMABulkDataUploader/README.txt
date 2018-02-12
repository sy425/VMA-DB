BulkDataUploader README
Author: Dave Krestynick

Included Source Files:
	- VMABulkDataUploader.py
	- Config.py (settings and defaults for the uploader)

----- Installation -----
You'll need to install the following on your machine:
	- Python 2.7: https://www.python.org/downloads/release/python-2714/
	- MySQL Driver for Python
		+ Windows: http://sourceforge.net/projects/mysql-python/files/mysql-python/1.2.3/MySQL-python-1.2.3.win32-py2.7.msi/download
		+ Mac: https://stackoverflow.com/questions/1448429/how-to-install-mysqldb-python-data-access-library-to-mysql-on-mac-os-x#1448476
		+ Linux: sudo apt-get install python-mysqldb

Once all the prerequisite software is installed, you should be good to run the Python program! Be sure 
that 

----- Usage -----
Via the command line, navigate to where the "VMABulkDataUploader.py" file is located on your machine. 
Then, as command line arguments, input each of the CSV table files you wish to upload. Here are a few 
examples of its usage:

Single Table: Py -2 VMABulkDataUploader.py appointment.csv

All Tables: Py -2 VMABulkDataUploader.py appointment.csv medicalprocedure.csv patient.csv postprocedurequestion.csv postprocedurequestionresponse.csv preprocedurequestion.csv preprocedurequestionnumber.csv specialinstruction.csv

The CSVs should be located in the same directory as the Python script as well. Do note, that by default, 
the configuration for this uploader is to DELETE ALL DATA contained in the database tables. This can be 
changed by editting the Config.py file, and changing the PURGE_TABLE_DATA_BEFORE_UPLOAD variable from 
True to False.

Another note, if you have both Python 3.6 and 2.7 installed, ensure you're running 2.7 on this Python 
script by using the "Py -2" command (as illustrated in the supplied examples). This ensures that you'll 
be using Python 2.7, as the connector module used in this script is only compatible with Python 2.7.