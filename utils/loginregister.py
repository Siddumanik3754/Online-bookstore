import mysql.connector

mydb =mysql.connector.connect(host="onlinebookstore.ccvpvj32idfp.ap-southeast-1.rds.amazonaws.com", user="admin", passwd="onlinebookstore", database="onlinebookstore")


# function to register customer
def register(mysql,username,fname,lname,email,password,phone,country,state,pincode,address):        
    cur = mydb.cursor()
    try:
        cur.execute("INSERT INTO Customers(customerID,firstName,lastName,address,pincode,country,phone,state,emailID,password) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(username,fname,lname,address,pincode,country,phone,state,email,password))
        result = 1 # registration successful
    except Exception as e:
        result =  0 # registration failed
    mydb.commit()
    cur.close()
    
    return result

# function for admin login
def adminLogin(mysql,username,password,account):
    cur = mydb.cursor()
    cur.execute("SELECT * from Admins WHERE adminID = %s AND password = %s",(username,password))
    check = cur.fetchall()
    check = list(check)

    if not check:
        result = 0 # login failed
    else:
        result = 1 # login success
    
    mydb.commit()
    cur.close()
    return result

# function for customer login
def customerLogin(mysql,username,password,account):
    cur = mydb.cursor()
    cur.execute("SELECT * from Customers WHERE customerID = %s AND password = %s",(username,password))
    check = cur.fetchall()
    check = list(check)

    if not check:
        result = 0 # login failed
    else:
        result = 1 # login success

    mydb.commit()
    cur.close()
    return result,check
