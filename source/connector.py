import mysql.connector
def create_connector():
    cnx = mysql.connector.connect(user='root', password='',
                            host='localhost',
                            database='libscrap')
    print(cnx)
    return cnx
create_connector()
