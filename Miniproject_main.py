import sqlite3
import re
from datetime import date,timedelta
import auth

conn=sqlite3.connect("Library.db")

c=conn.cursor()


class books:
    def addBook(self,isbn,title,author,genre,copy):
        try:
           result= c.execute("""
            INSERT INTO BOOKS (isbn, title, author, genre, available_copies)
            VALUES (?, ?, ?, ?, ?)
            """, (isbn,title,author,genre,copy)
            )
           if result:
               print("Book added Successfully!")
               conn.commit()
        except sqlite3.IntegrityError:
            print("Book already Entered ,Please add a new book")
    def updateBook(self,attribute,newcopy,key):
        if attribute=="ID/ISBN":
            c.execute ("""
            UPDATE BOOKS SET available_copies=?
            WHERE book_id=? or isbn=?
             """,
             (newcopy,int(key),key)
             )
        elif attribute=="TITLE":
            c.execute ("""
            UPDATE BOOKS SET available_copies=?
            WHERE title LIKE ? 
             """,
             (newcopy,key)
             )
        if c.rowcount>0:
            print("Available copies updated successfully!")
        else:
            print("Book is not found,please Enter Valid BookID/ISBN/Title")
        conn.commit()

    def deleteBook(self,bookID,title):
        query="""DELETE FROM BOOKS WHERE book_id=?"""
        result=c.execute(query,(bookID,))
        if result:
            print(f"{title} Was Deleted Successfully")
            conn.commit()
        else:
            print("Something Went Wrong,please try again")
        
    def getBookDetails(self,prompt):
        while True:
            key=input(prompt).strip()
            if key.isdigit() and key:
                query="SELECT * FROM BOOKS WHERE book_id=? or isbn=?"
                c.execute (query,(key,key))
                bookDetails=c.fetchall()
                if  bookDetails:
                    return bookDetails
                else:
                    print("Invalid Book ID/ISBN,Please try again")
            elif key:
                query="SELECT * FROM BOOKS WHERE title LIKE ? or author LIKE ?"
                c.execute(query,(f"%{key}%",f"%{key}%"))
                bookDetails=c.fetchall()
                if bookDetails:
                    return bookDetails
                else:
                    print("Book is not Found ,Please try again")
            elif not key: 
                print("Please Enter the Details")

    def addBorrowHistory(self,bookID,memberID,memberName,title):

        query="""SELECT * FROM BORROW_HISTORY WHERE book_id=? and member_id=?"""
        c.execute(query,(bookID,memberID))
        
        if c.fetchone is not None:
            print(f"{title} aleady Issued to {memberName}")
            return False
        borrowDate=date.today()
        dueDate=date.today() + timedelta(days=30)
        returnDate=""

        query="""INSERT INTO BORROW_HISTORY (book_id,member_id,member_name,title,borrow_date,due_date,return_date) 
                 VALUES (?,?,?,?,?,?,?) """
        
        result=c.execute(query,(bookID,memberID,memberName,title,borrowDate.isoformat(),dueDate.isoformat(),returnDate)) 
        conn.commit()
        if result:
            print(f"{title} successfully issued to {memberName}")
            return True
        else:
            print("Book issue Failed,Please try again")
            return False
    def updateBorrowHistory(self,bookID,memberID,currStatus,newStatus):
        returnDate=date.today().isoformat()
        getDuedate="""SELECT due_date,tracking_id from BORROW_HISTORY WHERE book_id=? AND member_id=? 
         AND status=?"""
        c.execute(getDuedate,(bookID,memberID,currStatus))
        row=c.fetchone()
        if row is not None:
            
            TrackingId=row[1]
            query="""UPDATE BORROW_HISTORY SET status=? ,return_date=? WHERE tracking_id=?"""
            result=c.execute(query,(newStatus,returnDate,TrackingId))
            conn.commit()
            if result:
                print("Book Returned Successfully ")
                return True
            else:
                return False
        else:
            duedate=None
            print("Borrow details not found for this BOOK/MEMBER")

        

        
    def promptISBN(self,prompt):
        while True:
            isbn=input(prompt).strip()
            isbnPattern=r"^(?:978|979)\d{10}$"
            if re.findall(isbnPattern,isbn):
                return isbn
            else:
                print("ISBN should be 13 digit number starting with 978 or 979")
                
    def promptTitle(self,prompt):
        while True:
            title=input(prompt).strip()
            if  not title:
                print("Title is required ,Enter again  ")
            else:
                return title
    def promptAuthor(self,prompt):
            while True:
                author=input(prompt).strip()
                if  not author:
                    print("Author is required ,Enter again  ")
                else:
                    return author
    def promptCopy(self,prompt):
        while True:
            try:
                copy=int(input(prompt))
                if copy <=0:
                    print("Number of copies must be greater than  zero, please try again ")
                else:
                    return copy
            except ValueError:
                print("Invalid Input,please try again")


class member:
    def promptName(self,prompt):
        while True:
            name=input(prompt).strip()
            if not name:
                print("First name is required,Enter again")
            else:
                return name;
    def promptEmail(self,prompt):
        email_pattern="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+[.][a-zA-Z]{2,}"

        while True:
            email=input(prompt).strip()
            if re.findall(email_pattern,email):
                return email
            else:
                print("Invalid email id ,enter a valid email")

    def promptMobileNu(self,prompt):
        while True:
            mobileNum=(input(prompt))
            if len(mobileNum) == 10 and mobileNum.isdigit():
                return mobileNum     
            else:
                print("Mobile number is invalid ,Enter valid 10 digit mobile number")
    def addMember(self,fname,lname,email,mobile,status):
        result= c.execute("""
            INSERT INTO MEMBER (first_name,last_name,email,phone,membership_status)
            VALUES (?, ?, ?, ?, ?)
            """, (fname,lname,email,mobile,status)
                )
        if result:
            print("Member added Successfully!")
            conn.commit()
    def getMemdetails(self,prompt):
        while True:
            key=input(prompt).strip()
            if key:
                if key.isdigit():
                    query="SELECT * FROM MEMBER WHERE member_id=?"
                    c.execute(query,(int(key),))
                    memberDetails=c.fetchall()
                    if memberDetails:
                        return memberDetails
                    else:
                        print("Member is not found,please try again")
                else:
                    query="SELECT * FROM MEMBER WHERE first_name LIKE ?"
                    c.execute(query,(key,))
                    memberDetails=c.fetchall()
                    if memberDetails:
                        return memberDetails
                    else:
                        print("Member is not found,please try again")
            else:
                print("Please enter the details ")

    def getMemberBorrowHistory(self,prompt,status,searchBy):
        while True:
            key=input(prompt).strip()
            if key:
                if key.isdigit():
                    if status=="Borrowed":
                        query="""SELECT * FROM BORROW_HISTORY WHERE member_id=? AND status=?"""
                        c.execute(query,(int(key),status))
                        memberBorrowDetails=c.fetchall()
                        if memberBorrowDetails:
                            return memberBorrowDetails
                        else:
                            print("No Borrow History found for this Member")
                            return []
                    elif status=="All":
                        query="""SELECT * FROM BORROW_HISTORY WHERE member_id=?"""
                        c.execute(query,(int(key),))
                        memberBorrowDetails=c.fetchall()
                        if memberBorrowDetails:
                            return memberBorrowDetails
                        else:
                            print("No Borrow History found for this Member")
                            return []
                else:
                    if searchBy=="ID/NAME":
                        query="""SELECT * FROM BORROW_HISTORY WHERE member_name LIKE ?"""
                        c.execute(query,(f"%{key}%",))
                        memberBorrowDetails=c.fetchall()
                        if memberBorrowDetails:
                            return memberBorrowDetails
                        else:
                            print("No Borrow History found for this Member")
                            return []
            else:
                print("Please enter the details")
    def updateMember(self, memberID, attribute, newValue):
        if attribute == "EMAIL":
            query = "UPDATE MEMBER SET email=? WHERE member_id=?"
        elif attribute == "PHONE":
            query = "UPDATE MEMBER SET phone=? WHERE member_id=?"
        
        c.execute(query, (newValue, memberID))
        if c.rowcount > 0:
            print("Member details updated successfully!")
        else:
            print("Update failed, please try again")
        conn.commit()
                        


                                                  
b=books()
m=member()
MENU = """
Choose one option:
1. Add New Book
2. Update Available Copies
3. Add New Member
4. Issue Book to Member
5. Return Book
6. Search Book
7. View Borrow History
8. Delete Book
9. Update Member Details
10. Exit
"""


def main():
    user_id, name, username = auth.authenticate()
    while True:
        print(MENU)
        option=int(input())

        if option==1:
            print("***ADD NEW BOOK***")
            isbn=b.promptISBN("Enter ISBN:")    
            title=b.promptTitle("Enter Title:")
            author=b.promptAuthor("Enter Author:")
            genre=input("Enter Genre: ").strip()
            copy=b.promptCopy("Enter Number of Copies:")
            b.addBook(isbn,title,author,genre,copy)
          
        if option==2:
            print("***UPDATE BOOK DETAIL***")    
            key=input("Enter BookID/ISBN/Title of the Book: ") 
            try:
                newcopy=int(input("Update Available Copies to: "))
                if key.isdigit():
                    b.updateBook("ID/ISBN",newcopy,key)
                else:
                    b.updateBook("TITLE",newcopy,key)
            except ValueError:
                print("Available copies should be Numeric value")
         
        elif option==3:
            print("***ADD NEW MEMBER***")
            fname=m.promptName("Enter first Name :")
            lname=input("Enter Last Name : ").strip()
            email=m.promptEmail("Enter Email : ")
            mobileNumber=int(m.promptMobileNu("Enter Mobile Number :"))
            status="Active"
            m.addMember(fname,lname,email,mobileNumber,status)
        elif option==4:
            print("***ISSUE BOOK TO MEMBER***")
            bookDetails=b.getBookDetails("Enter Book ID/ISBN: ")
            memberDetails=m.getMemdetails("Enter Membership ID: ")
            print("BOOK DETAILS:")
            for book in bookDetails:
                print("TITLE : ",book[2])
                print("AUTHOR: ",book[3])
                bookid=book[0]
                title=book[2]
                newcopy=book[5]-1
            print("MEMBER DETAILS:")
            for member in memberDetails:
                print("Member Name:",member[1],member[2])
                memid=member[0]
                memname=member[1]+" "+member[2]
            if b.addBorrowHistory(bookid,memid,memname,title):
                b.updateBook("ID/ISBN",newcopy,bookid)
        elif option==5:
            print("***RETURN BOOK***")
            
            memberBorrowDetails=m.getMemberBorrowHistory("Enter Membership ID:","Borrowed"," ")
            if memberBorrowDetails:           
                print("***BORROW DETAILS FOR THE MEMBER***")
                for borrowDetail in memberBorrowDetails:
                    print("BOOK ID : ",borrowDetail[1])
                    print("Title: ",borrowDetail[4])
                    memid=borrowDetail[2]
                bookDetails=b.getBookDetails("Enter Book ID to return: ") 
                for book in bookDetails:
                    bookid=book[0] 
                    newcopy=book[5]+1  
                if b.updateBorrowHistory(bookid,memid,"Borrowed","Returned"):
                    b.updateBook("ID/ISBN",newcopy,bookid)
        elif option==6:
            print("***SEARCH BOOK***")
            bookDetails=b.getBookDetails("Enter BookID/ISBN/Title/Author:")
            for book in bookDetails:
                print("TITLE : ",book[2])
                print("AUTHOR: ",book[3])
                print("AVAILABLE COPIES:",book[5])

        elif option==7:
            print("View Borrow History")
            memberBorrowDetails=m.getMemberBorrowHistory("Enter Member ID/Name:","All","ID/NAME")
            for borrowDetail in memberBorrowDetails:
                print("BOOK ID         :",borrowDetail[1])
                print("MEMBER ID       :",borrowDetail[2])
                print("MEMBER NAME     :",borrowDetail[3])
                print("TITLE           :",borrowDetail[4])
                print("BORROW DATE     :",borrowDetail[5])
                print("DUE DATE        :",borrowDetail[6])
                print("RETURN DATE     :",borrowDetail[7])
                print("STATUS          :",borrowDetail[8])
                print("\n")

        elif option==8:
            print("***DELETE BOOK***") 
            bookDetails=b.getBookDetails("Enter Book ID/ISBN: ")
            for books in bookDetails:
                bookID=books[0]
                title=books[2]
            deleteConfirm=input(f"{title} will be Deleted Permeantenly ,Do you wish to continue ? Y/N: ").upper()
            if deleteConfirm=="Y":
                b.deleteBook(bookID,title)
        elif option==9:
            print("***UPDATE MEMBER DETAILS***")
            memberDetails=m.getMemdetails("Enter Member ID/First Name: ")
            for member in memberDetails:
                print("MEMBER ID         :",member[0])
                print("MEMBER NAME       :",member[1],member[2])
                print("EMAIL             :",member[3])
                print("PHONE             :",member[4])
                print("MEMBERSHIP STATUS :",member[5])
                memid=member[0]

            if len(memberDetails) > 1:
                memid = int(input("Multiple members found. Enter exact Member ID to update: "))

            print("\nWhat would you like to update?\n1. Email ID\n2. Phone Number")
            choice=input("Enter choice (1 or 2): ").strip()

            if choice=="1":
                newEmail=m.promptEmail("Enter New Email: ")
                m.updateMember(memid,"EMAIL",newEmail)
            elif choice=="2":
                newPhone=int(m.promptMobileNu("Enter New Mobile Number: "))
                m.updateMember(memid,"PHONE",newPhone)
            else:
                print("Invalid choice, returning to menu")
         
        elif option==10:
            break;
    
    conn.commit()
    conn.close()

main()



