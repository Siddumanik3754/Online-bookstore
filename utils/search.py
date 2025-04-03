import mysql.connector

mydb =mysql.connector.connect(host="onlinebookstore.ccvpvj32idfp.ap-southeast-1.rds.amazonaws.com", user="admin", passwd="onlinebookstore", database="onlinebookstore")


def searchTitle(mysql,query):
    cur = mydbn.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE title LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    booksData = list(cur.fetchall())
    mydb.commit()
    cur.close()
    return booksData

def searchGenre(mysql,query):
    cur = mydb.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b, Authors as a WHERE b.genre LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    booksData = list(cur.fetchall())
    mydb.commit()
    cur.close()
    return booksData

def searchAuthor(mysql,query):
    cur = mydb.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.firstName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    list1Data = list(cur.fetchall()) # search query matching with the first name of the author
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b,Authors as a WHERE a.lastName LIKE %s AND b.authorID = a.authorID",({'%' + query + '%'}))
    list2Data = list(cur.fetchall()) # search query matching with the last name of the author
    booksData = list(set(list1Data) | set(list2Data))   # without repition
    mydb.commit()
    cur.close()
    return booksData