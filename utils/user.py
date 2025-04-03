import mysql.connector

mydb =mysql.connector.connect(host="onlinebookstore.ccvpvj32idfp.ap-southeast-1.rds.amazonaws.com", user="admin", passwd="onlinebookstore", database="onlinebookstore")


def admin(mysql):
    cur = mydb.cursor()
    cur.execute("SELECT * from Admins")
    adminData = list(cur.fetchall())
    mydb.commit()
    cur.close()
    return adminData

def customers(mysql):
    cur = mydb.cursor()
    cur.execute("SELECT * from Customers")
    customerData = list(cur.fetchall())
    mydb.commit()
    cur.close()
    return customerData

def adminAccount(mysql,userID):
    cur = mydb.cursor()
    cur.execute("SELECT * from Admins WHERE adminID = %s",(userID,))
    Data = list(cur.fetchone())
    mydb.commit()
    cur.close()
    return Data

def customerAccount(mysql,userID):
    cur = mydb.cursor()
    cur.execute("SELECT * from Customers WHERE customerID = %s",(userID,))
    customerData = list(cur.fetchone())
    mydb.commit()
    cur.close()
    return customerData

def contactUs(mysql,fname,lname,email,message,timestamp):
    cur = mydb.cursor()

    try:
        cur.execute("INSERT INTO ContactUs(firstName,lastName,emailID,message,timestamp) VALUES (%s,%s,%s,%s,%s)",(fname,lname,email,message,timestamp))
        result = 1 # insert successful
    except:
        result = 0 # insert unsuccessful

    mydb.commit()
    cur.close()
    return result