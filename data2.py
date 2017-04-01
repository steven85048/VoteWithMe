import pyodbc
server = 'votewithme.database.windows.net'
database = 'votewithme'
username = 'admin_votewithme@votewithme'
password = '!sQ9XU%8I5@qw2wZ'
driver= '{ODBC Driver 13 for SQL Server}'
cnxn = pyodbc.connect('DRIVER='+driver+';PORT=1433;SERVER='+server+';PORT=1443;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = cnxn.cursor()
cursor.execute("CREATE TABLE bill (bill_id VARCHAR(20), last_updated DATETIME, latest_action VARCHAR(20), state VARCHAR)")
