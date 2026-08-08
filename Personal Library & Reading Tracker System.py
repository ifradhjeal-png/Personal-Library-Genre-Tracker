import sqlite3

class LibraryManager:
    def __init__(self,db_file_name):#Parameterized constructor
        self.db_file_name=db_file_name
        self.conn=sqlite3.connect(self.db_file_name)
        self.cur=self.conn.cursor()

    def Create_Table(self):
        Books_Table='''CREATE TABLE IF NOT EXISTS BOOKS_TABLE
        (BOOK_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        BOOK_TITLE TEXT NOT NULL,
        BOOK_AUTHOR TEXT NOT NULL,
        BOOK_PAGES INTEGER NOT NULL,
        BOOK_GENRE VARCHAR(50) NOT NULL)''' 
        self.cur.execute(Books_Table)

    def import_from_txt(self,file):
        self.file=file
        try:
            sql_query="INSERT INTO BOOKS_TABLE (BOOK_TITLE, BOOK_AUTHOR, BOOK_PAGES, BOOK_GENRE) VALUES (?, ?, ?, ?)"
        except sqlite3.Error as e:
            print(e)    
        try:
            with open(file,"r") as f:
                Books_data=f.readline()
                while Books_data:
                    Books_data=Books_data.split(",")
                    self.cur.execute(sql_query,Books_data)
                    Books_data=f.readline()
        except FileNotFoundError:
            print("File dont exist in this folder!")

        except Exception as e:
            print(f'An error has occured {e}')   

    def load_books(self):
        #getting data
        #unpacking the list
        Sql_query="SELECT * FROM BOOKS_TABLE"
        self.cur.execute(Sql_query)
        for i in self.cur.fetchall():
            print(i)

    def get_unique_genres(self):
        Set_genre=set()
        try:
            with open(self.file,"r")as f:
                Books_data=f.readline()
                while Books_data:
                    List_Books_data=Books_data.split(",")
                    String_Data=List_Books_data[len(List_Books_data)-1]
                    Set_genre.add(String_Data[0:len(String_Data)-1])
                    Books_data=f.readline()
        except FileNotFoundError:
            print("The file dont exist in the folder!")
        except Exception as e:
            print(f'An error has occured {e}')
        return Set_genre

    def get_genre_summary(self):
        Dict_summary={}
        Set_Duplicates_names=set()
        try:
            sql_query="SELECT * FROM BOOKS_TABLE"
            self.cur.execute(sql_query)
            List_data=self.cur.fetchall()
            Track_1=0
            for i in List_data:
                count=0
                Genre=i[-1]
                Genre=Genre[0:len(Genre)-1]
                Track_1=0   
                for j in List_data:
                    temp_genre=j[-1]
                    temp_genre=temp_genre[0:len(temp_genre)-1]
                    if(Track_1==len(List_data)-1):
                        temp_genre=j[-1]    
                    if(Genre in Set_Duplicates_names):
                        break

                    if(Genre==temp_genre):
                        count+=1
                    Track_1+=1
                if(Genre not in Set_Duplicates_names and count!=0):
                    Dict_summary.update({Genre:count})        
                Set_Duplicates_names.add(Genre)  
        except FileNotFoundError:
            print("The file dont exist in the folder!")
            return "Null"
        except Exception as e:
            print(f'An error has occured {e}')
            return "Null"
        return Dict_summary

    def Get_Total_Books(self,file_name):
        try:
            with open(file_name,"r") as f:
                count=0
                Books_Data=f.readline()
                while Books_Data:
                    count+=1
                    Books_Data=f.readline()    
        except FileNotFoundError:
            print("The file doesnt exist in this folder!")
            return
        except Exception as e:
            print(f'An error has occured {e}')
            return   
        return count         

    
    def export_report(self,Library_file_name):
        with open(Library_file_name,"w") as f:
            Total_Books=self.Get_Total_Books("BOOKS.txt")
            f.write(f"Total Books is : {Total_Books}\n")
            f.write(f'Unique Genres : \n')
            f.write(f'{str(self.get_unique_genres())}\n')
            f.write("Genre Breakdown : \n")
            f.write(str(self.get_genre_summary()))

#Blueprint of the data                    
class Book:
    def __init__(self):
        pass
    def title(self,title):
        self.Book_title=(title)
    def Book_author(self,author):
        self.author=author
    def Book_Pages(self,pages):
        self.pages=int(pages)
    def Book_genre(self,genre):
        self.genre=genre        




print("--- LIBRARY SUMMARY REPORT ---")

# 1. Initialize manager (connects to SQLite & creates table if needed)
manager = LibraryManager("library.db")
manager.Create_Table()
# 2. Read from a text file and add to SQLite database
manager.import_from_txt("BOOKS.txt")

# 3. Fetch books from SQLite (stored as list of tuples) and load as Book objects
manager.load_books()

# 4. Perform Data Structure Analysis
unique_genres = manager.get_unique_genres()  # Returns a set
print(unique_genres)
genre_counts = manager.get_genre_summary()   # Returns a dict
print(genre_counts)

 #5. Export summary to a text file
manager.export_report("library_summary.txt")