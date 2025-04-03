import mysql.connector

mydb =mysql.connector.connect(host="onlinebookstore.ccvpvj32idfp.ap-southeast-1.rds.amazonaws.com", user="admin", passwd="onlinebookstore", database="onlinebookstore")


# function to get all books
def allBooks(mysql):
    cur = mydb.cursor()
    cur.execute("SELECT b.bookID,a.authorID,b.publisherID,b.title,b.genre,b.publicationYear,b.price,a.firstName,a.lastName FROM Books as b INNER JOIN Authors as a ON b.authorID = a.authorID  ORDER BY bookID")
    booksData = cur.fetchall()
    booksData = list(booksData)
    mydb.commit()
    cur.close()
    return booksData

# function to get all genre
def allGenre(mysql):
    cur = mydb.cursor()
    cur.execute("SELECT DISTINCT genre from Books")
    genreData = list(cur.fetchall())
    mydb.commit()
    cur.close()
    return genreData