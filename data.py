import pycurl
import certifi
import json
import pyodbc
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO
	
from flask import Flask
app = Flask(__name__)
	
# --- SETTING UP DATABASE CONNECTION AND MAINTAINING CNXN AS A GLOBAL VARIABLE ---
server = 'lahacks.database.windows.net'
database = 'votewithme'
username = 'admin_voteforme@lahacks'
password = 'password1$'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()

# --- SETTING UP THE PYCURL OBJECT
c = pycurl.Curl()
c.setopt(pycurl.CAINFO, certifi.where())

# ============================================================================#
# ============= UTILITY METHODS ==============================================#
# ============================================================================#

# --- RUN TO RESET TABLES IN DATABASE ---
def init():
	#cursor.execute("CREATE TABLE user_identification (email VARCHAR(20) UNIQUE, password VARCHAR(20) NOT NULL, interest VARCHAR(20),zip_district VARCHAR(20))")
	cursor.execute("CREATE TABLE legislation (bill_id VARCHAR(20) NOT NULL UNIQUE , last_updated DATE, latest_action VARCHAR(256), state VARCHAR(10) NOT NULL, level VARCHAR(30), votes_pos INT, votes_neg INT)")

def printDatabaseContents():
	cursor.execute("SELECT * FROM legislation")
	
	for row in cursor.fetchall():
		print(row)
		
def shutDown():
	# --- Commit the Connection Changes
	cnxn.commit()

	# --- Close the pycurl object
	c.close()
	
# ============================================================================#
# ============= METHODS TO CONTINUALLY UPDATE BILL DATA ======================#
# ============================================================================#
	
# --- TAKES BILL DATA AS PARAMS AND SAVES INTO DATABASE
def saveBillData(data):
	for i in data:
		currId = i['bill_id'];
		last_action = i['latest_major_action'];
		state = i['active']
		
		# check if duplicate
		cursor.execute("SELECT * FROM legislation WHERE bill_id = '" + currId + "'");
		
		# if there exists a unique entry, add into database
		if (not cursor.fetchall()):
			print(last_action)
			print(currId)
			cursor.execute("INSERT INTO legislation (bill_id, last_updated, latest_action, state) VALUES ('"+currId+"', GETDATE(),'" + last_action + "', 'true')")
			
# --- UPDATES THE BILLS CURRENTLY IN THE DATABASE 
def updateBillsInDatabase():
	cursor.execute("SELECT * FROM legislation")
	
	buffer = BytesIO()
	c.setopt(c.HTTPHEADER, ['X-API-Key: 4jVRBAKrhn4nniRoSo5Gf4AWuM8DaA9G3GUC9pqN'])
	c.setopt(c.WRITEDATA, buffer);
		
	# Fetches entire list of the contents of the legislation database
	for row in cursor.fetchall():
		print(row);
		cursor.execute("UPDATE legislation SET latest_action = '"+ row[2]+"', last_updated = GETDATE() WHERE bill_id = '" + row[0] + "'");
		c.setopt(c.URL, 'https://api.propublica.org/congress/v1/115/bills/' + row[0])
		c.perform()
			
# --- GETS JSON LIST OF CURRENTLY UPDATED BILLS FROM API ---
def getIntroducedBills():	
	buffer = BytesIO();
	c.setopt(c.URL, 'https://api.propublica.org/congress/v1/115/senate/bills/introduced.json')
	c.setopt(c.HTTPHEADER, ['X-API-Key: 4jVRBAKrhn4nniRoSo5Gf4AWuM8DaA9G3GUC9pqN'])
	c.setopt(c.WRITEDATA, buffer);
	c.perform()

	data = buffer.getvalue().decode('UTF-8')

	# ---- GET LIST OF BILLS ----
	jso = json.loads(data);
	saveBillData(jso['results'][0]['bills']);
	
	# HTTP response code, e.g. 200.
	print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
	# Elapsed time for the transfer.
	print('Status: %f' % c.getinfo(c.TOTAL_TIME))
	
# ============================================================================#
# ============= ROUTES TO OBTAIN DATA FROM THE API ===========================#
# ============================================================================#
	
# --- GETS LIST OF BILLS SORTED BY DATE
@app.route('/getBillsSortedId', methods = ['GET']
def getBillsSortedId():
	cursor.execute("SELECT * FROM legislation ORDER BY bill_id DESC");
	
	total_json_data = [];
	for row in cursor.fetchall():
		data = {"id": row[0], "last_update": row[2], "upvote": row[5], "downvote": row[6]};
		total_json_data.append(data);
		
	return (json.dumps(total_json_data))
	
# --- GETS JSON OF BILL USING ID STORED IN DB
# --- SEND BILL ID IN POST BODY 
# --- NOTE: SEARCH BY NUMBER BEFORE DASH IN BILL_ID: (e.g. s782-115 would be s782 as the query)
@app.route('/getBillById/<string:id>', methods = ['GET'])
def getBillById(id):
	buffer = BytesIO();
	c.setopt(c.URL, 'https://api.propublica.org/congress/v1/115/bills/' + id)
	c.setopt(c.HTTPHEADER, ['X-API-Key: 4jVRBAKrhn4nniRoSo5Gf4AWuM8DaA9G3GUC9pqN'])
	c.setopt(c.WRITEDATA, buffer);
	c.perform()

	data = buffer.getvalue().decode('UTF-8')
	print(data)
	jso = json.loads(data);
	
	# HTTP response code, e.g. 200.
	print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
	# Elapsed time for the transfer.
	print('Status: %f' % c.getinfo(c.TOTAL_TIME))
	
	return jso;


# -- TAKES LEGISLATOR AS PARAMETER (FIRST_NAME LAST_NAME e.g. Elizabeth Warren) AND RETURNS THE JSON DATA FOR LEGISLATOR 
# -- STORE MEMBER NAME IN POST BODY
@app.route('/getMemberId/<string:legislator>', methods = ['GET'])
def getMemberId(legislator):
	buffer = BytesIO();
	
	c.setopt(c.URL, 'https://api.propublica.org/congress/v1/115/senate/members.json')
	c.setopt(c.HTTPHEADER, ['X-API-Key: 4jVRBAKrhn4nniRoSo5Gf4AWuM8DaA9G3GUC9pqN'])
	c.setopt(c.WRITEDATA, buffer);
	c.perform()

	data = buffer.getvalue().decode('UTF-8')
	
	# ---- FIND THE LEGISLATOR ---- #
	
	jso = json.loads(data)
	num_legislators = int(jso['results'][0]['num_results']);
	
	legislatorInfo = "EMPTY";
	for i in range(0, num_legislators): #checks according to first and last names
		first_name = jso['results'][0]['members'][i]['first_name'];
		last_name = jso['results'][0]['members'][i]['last_name'];
		if (first_name in legislator and last_name in legislator):
			legislatorInfo = jso['results'][0]['members'][i]
			break;
		
	print(legislatorInfo);
		
	# HTTP response code, e.g. 200.
	print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
	# Elapsed time for the transfer.
	print('Status: %f' % c.getinfo(c.TOTAL_TIME))
	
	return legislatorInfo;

# ============================================================================#
# ============= TESTING METHODS ==============================================#
# ============================================================================#
	
# --- Initialize the Tables ---
#init()

# --- Run to add most recent bills ---
#getIntroducedBills()

# --- Run to update bills currently in database ---
#updateBillsInDatabase()

# --- Final bill display
#printDatabaseContents()

# --- Test getBillsById
#getBillsById()

