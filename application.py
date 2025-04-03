from flask import Flask,jsonify,request,render_template,redirect,url_for,session
# from Flask_MySQL import MySQL
import re,datetime,os
import requests


from utils.home import *
from utils.loginregister import *
from utils.book import *
from utils.search import *
from utils.user import *
from utils.orders import *




application = Flask(__name__)



application.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # all the session data is encrypted in the server so we need a secret key to encrypt and decrypt the data




# home page route
@application.route("/")
def homeRoute():
    booksData = allBooks(mysql)
    genreData = allGenre(mysql)
    return render_template("home.html",booksData=booksData,genreData=genreData)

# home page for customers
@application.route("/customerindex",methods=["POST","GET"])
def customerindexRoute():
    if 'userID' in session:
        booksData = allBooks(mysql)
        genreData = allGenre(mysql)
        return render_template("customerindex.html",booksData=booksData,genreData=genreData)
    else:
        return redirect(url_for('loginRoute'))

# home page for admins
@application.route("/adminindex",methods=["POST","GET"])
def adminindexRoute():
    booksData = allBooks(mysql)
    genreData = allGenre(mysql)
    return render_template("adminindex.html",booksData=booksData,genreData=genreData)

# Customer Registration route
@application.route("/register",methods=["POST","GET"])
def registerRoute():
    if request.method == "POST":
        username = str(request.form.get("username"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        password = str(request.form.get("password"))
        phone = str(request.form.get("phone"))
        country = str(request.form.get("country"))
        state = str(request.form.get("state"))
        pincode = int(request.form.get("pincode"))
        address = str(request.form.get("address"))

        response = register(mysql,username,fname,lname,email,password,phone,country,state,pincode,address)
        
        if response == 1: # regsitration is successful
            return render_template("login.html",response=response)
        else: # registration failed
            return render_template("register.html",response=response)

    return render_template("register.html")

# login for customers and admins route
@application.route("/login",methods=["POST","GET"])
def loginRoute():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        account = request.form.get("account")

        if account=="customer":
            response,data = customerLogin(mysql,username,password,account)
            if response == 1: # login success
                session["userID"] = username # creating a session of the username
                session["accountType"] = account # creating a session of the account type
                for i in data:
                    session["email"] = i[3] # creating a session of email
                return redirect(url_for("customerindexRoute"))
            else: # Login failed
                return render_template("login.html",response = response)

        if account=="admin":
            response = adminLogin(mysql,username,password,account)
            if response == 1: # login success
                session["userID"] = username # creating a session of the username
                session["accountType"] = account # creating a session of the account type
                return redirect(url_for("adminindexRoute"))
            else: # login failed
                return render_template("login.html",response=response)

    return render_template("login.html")

# search books in admin portal
@application.route("/search",methods=["POST","GET"])
def searchRoute():
    if 'userID' in session:
        if request.method == "POST":
            search = str(request.form.get("search"))
            query = str(request.form.get("query"))

            if search == "title": # search by title
                booksData = searchTitle(mysql,query)
                return render_template("search.html",booksData=booksData,search=search)
            
            if search == "genre": # search by genre
                booksData = searchGenre(mysql,query)
                return render_template("search.html",booksData=booksData,search=search)
            
            if search == "author": # search by author
                booksData = searchAuthor(mysql,query)
                return render_template("search.html",booksData=booksData,search=search)

            return render_template("search.html")
        
        return render_template("search.html")
    else:
        return redirect(url_for('loginRoute'))

# search books in admin portal
@application.route("/customersearch",methods=["POST","GET"])
def customersearchRoute():
    
    if request.method == "POST":
        search = str(request.form.get("search"))
        query = str(request.form.get("query"))

        if search == "title": # search by title
            booksData = searchTitle(mysql,query)
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "genre": # search by genre
            booksData = searchGenre(mysql,query)
            return render_template("customersearch.html",booksData=booksData,search=search)
        
        if search == "author": # search by author
            booksData = searchAuthor(mysql,query)
            return render_template("customersearch.html",booksData=booksData,search=search)

        return render_template("customersearch.html")
    
    return render_template("customersearch.html")

# Add/Delete/Update Book Route for Admin
@application.route("/books",methods=["POST","GET"])
def booksRoute():
        booksData = allBooks(mysql)
        genreData = allGenre(mysql)
        return render_template("books.html",booksData=booksData,genreData=genreData)

# Add Book Route
@application.route("/addBook",methods=["POST","GET"])
def addBookRoute():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        title = str(request.form.get("title"))
        genre = str(request.form.get("genre"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        year = str(request.form.get("year"))
        price = str(request.form.get("price"))
        country = str(request.form.get("country"))
        stock = str(request.form.get("stock"))

        response = addBook(mysql,bookID,title,genre,fname,lname,year,price,country,stock)
        if response == 1: # Book Added Successfully
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)
        else: # book failed to add
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

    return redirect(url_for("booksRoute"))

# Update Book Route
@application.route("/updateBook",methods=["POST","GET"])
def updateBookRoute():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        price1 = str(request.form.get("price1"))
        price2 = str(request.form.get("price2"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        response = updateBook(mysql,bookID,price1,price2,fname,lname,country)
        if response == 1: # book updated successfully
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

        else: # book failed to update
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

    return redirect(url_for("booksRoute"))

# delete book Route
@application.route("/deleteBook",methods=["POST","GET"])
def deleteBookRoute():
    if request.method == "POST":
        bookID = str(request.form.get("bookID"))
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        country = str(request.form.get("country"))

        response = deleteBook(mysql,bookID,fname,lname,country)
        if response == 1: # book deleted successfully
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

        else: # book failed to delete
            booksData = allBooks(mysql)
            genreData = allGenre(mysql)
            return render_template("books.html",booksData=booksData,genreData=genreData,response=response)

    return redirect(url_for("booksRoute"))

# display book details route for customers
@application.route("/bookdetail<subject>",methods=["POST","GET"])
def bookDetailsRoute(subject):
    if 'userID' in session:
        bookData = bookDetail(mysql,subject)
        return render_template("bookdetail.html",bookData=bookData)
    else:
        return redirect(url_for('loginRoute'))
# display book details route for admin
@application.route("/bookDetailsAdmin<subject>",methods=["POST","GET"])
def bookDetailsAdminRoute(subject):
    bookData = bookDetail(mysql,subject)
    return render_template("bookdetail2.html",bookData=bookData)

# inventory route
@application.route("/inventory",methods=["POST","GET"])
def inventoryRoute():
    bookData = inventory(mysql)
    return render_template("inventory.html",bookData=bookData)

# buy book route
@application.route("/buyBook<bookID>",methods=["POST","GET"])
def buyBookRoute(bookID):
    if 'userID' in session:
        if request.method =="POST":
            quantity = str(request.form.get("quantity"))
            bookData = totalBookPrice(mysql,bookID,quantity)
            totalPrice = int(bookData[1]) * int(quantity)
            session['book']=bookData
            session['price']=totalPrice
            return render_template("payment.html",bookData=bookData,quantity=quantity,totalPrice=totalPrice)
            
        return "USE POST METHOD ONLY"
    else:
        return redirect(url_for('loginRoute'))
    
# pay order route
@application.route("/pay<isbn>/<quantity>/<total>",methods=["POST","GET"])
def payRoute(isbn,quantity,total):
    if 'userID' in session:
        if request.method =="POST":
            pay = str(request.form.get("pay"))
            API_URL2="https://9m9m6au2h2.execute-api.eu-west-1.amazonaws.com/prod/id"
            try:
                
                response = requests.get(API_URL2, stream=True)
                if response.status_code == 200:
                    data=response.json()
                    orderid=data.get('body')
                    print("OrderId generated Successfully ")
                else:
                    print(response)
                    print("Failed to generate OrderId")
            except Exception as e:
                print( f"An error occurred: {str(e)}")
            response = orders(mysql,isbn,quantity,total,pay,session["userID"],orderid)
            session['orderid']=orderid
            return redirect(url_for('orderconfirmationRoute',response = response))
            

        return "USE POST METHOD ONLY"   
    else:
        return redirect(url_for('loginRoute'))

# order confirmation route
@application.route("/orderconfirmation<response>",methods=["POST","GET"])
def orderconfirmationRoute(response):
    if 'userID' in session:

        book=session['book']
        price=session['price']
        email=session['email']
        answer=response
        orderid=session['orderid']
        
        


        API_URL = "http://x22183744-scalableapi.eba-gutq8iva.ap-northeast-1.elasticbeanstalk.com/email"
        try:
            subject='Order place for StoryScape '
            message=f"Your Order has been sucessfully placed for {book[2]} Rs {price}. Your order id is {orderid}. Thankyou for shopping!"
            data=f'{subject} : {message} : {email}'
            ##translating the name
            json_data = {"text": data }
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                
                print("Mail delivered Successfully ")
            else:
                print(response)
                print("Failed to email")
        except Exception as e:
            return f"An error occurred: {str(e)}"
        session.pop("price",None)
        session.pop("book",None)
        session.pop("orderid",None)
        return render_template("orderconfirmation.html",response=answer)
    else:
        return redirect(url_for('loginRoute'))

# display users route
@application.route("/users",methods=["POST","GET"])
def usersRoute():
    adminData = admin(mysql)
    customerData = customers(mysql)
    return render_template("users.html",adminData=adminData,customerData=customerData)

# display  orders in customers and admins account account
@application.route("/myorders",methods=["POST","GET"])
def ordersRoute():
    if 'userID' in session:
        userID = session["userID"]
        accountType = session["accountType"]

        if session["accountType"] == None or session["userID"]== None:
            return "ERROR"

        if session["accountType"]=="admin":
            Data = allorders(mysql,userID)
            return render_template("myorders.html",Data=Data,accountType=accountType)

        if session["accountType"]=="customer":
            Data = myorder(mysql,userID)
            return render_template("myorders.html",Data=Data,accountType=accountType)
        
        return "ERROR"
    else:
        return redirect(url_for('loginRoute'))

# display logged in users account
@application.route("/myaccount",methods=["POST","GET"])
def myAccountRoute():
    if 'userID' in session:
        userID = session["userID"]
        accountType = session["accountType"]

        if session["accountType"] == None or session["userID"]== None:
            return "ERROR"

        if session["accountType"]=="admin":
            Data = adminAccount(mysql,userID)
            return render_template("myaccount.html",Data=Data,accountType=accountType)

        if session["accountType"]=="customer":
            Data = customerAccount(mysql,userID)
            return render_template("myaccount.html",Data=Data,accountType=accountType)
        
        return "ERROR"
    else:
        return redirect(url_for('loginRoute'))

# contact us route
@application.route("/contactUs",methods=["POST","GET"])
def contactUsRoute():
    if request.method == "POST":
        fname = str(request.form.get("fname"))
        lname = str(request.form.get("lname"))
        email = str(request.form.get("email"))
        message = str(request.form.get("message"))
        timestamp = datetime.datetime.now()
        response = contactUs(mysql,fname,lname,email,message,timestamp)
        if response == 1:
            return "Message Submitted"
        else:
            return "Failed to add message"
            
    return "Use POST METHOD ONLY"

# logout route
@application.route("/logout",methods = ["GET","POST"])
def logoutRoute():
    session.pop("userID",None) # removing username from session variable
    session.pop("accountType",None) # removing account from session variable
    booksData = allBooks(mysql)
    genreData = allGenre(mysql)
    return render_template("home.html",booksData=booksData,genreData=genreData)


if __name__ == "__main__":
    application.run(debug=True,port=5050)
