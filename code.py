from tkinter import *
from tkinter import ttk
import tkinter.messagebox as MessageBox
import mysql.connector as sql

# Database connection function
def connect_db():
    return sql.connect(host="localhost", user="root", password="riya123", database="mydata")
def fetch_data():
    try:
        con = connect_db()
        cursor = con.cursor()
        query = "SELECT * FROM pharmacy"
        cursor.execute(query)
        rows = cursor.fetchall()
        if len(rows) != 0:
            pharmacy_table.delete(*pharmacy_table.get_children())
            for row in rows:
                pharmacy_table.insert('', END, values=row)
            con.commit()
        cursor.close()
        con.close()
    except Exception as e:
        MessageBox.showerror("Error", f"Error fetching data: {str(e)}")

# Insert function
def Insert():
    # Fetch values from entries
    REFRENCENO = REFRENCENO_entry.get()
    MEDICINETYPE = MEDICINETYPE_entry.get()
    MEDICINENAME = MEDICINENAME_entry.get()
    LOTNO = LOTNO_entry.get()
    ISSUEDATE = ISSUEDATE_entry.get()
    EXPDATE = EXPDATE_entry.get()
    DOSAGE = DOSAGE_entry.get()
    PRICE = PRICE_entry.get()
    PRODUCTQT = PRODUCTQT_entry.get()
    
    # Validate required fields
    if REFRENCENO == "" or MEDICINETYPE == "" or MEDICINENAME == "":
        MessageBox.showinfo("ALERT", "Please enter all fields")
    else:
        try:
            con = connect_db()
            cursor = con.cursor()
            query = "INSERT INTO pharmacy (REFRENCENO, MEDICINETYPE, MEDICINENAME, LOTNO, ISSUEDATE, EXPDATE, DOSAGE, PRICE, PRODUCTQT) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            values = (REFRENCENO, MEDICINETYPE, MEDICINENAME, LOTNO, ISSUEDATE, EXPDATE, DOSAGE, PRICE, PRODUCTQT) 
            cursor.execute(query, values)
            con.commit()
            cursor.close()
            con.close()
            MessageBox.showinfo("Status", "Successfully Inserted")
            
            reset_fields()
            fetch_data()
        except Exception as e:
            MessageBox.showerror("Error", f"Error inserting into database: {str(e)}")

# Update function
def Update():
    
    REFRENCENO = REFRENCENO_entry.get()
    MEDICINETYPE = MEDICINETYPE_entry.get()
    MEDICINENAME = MEDICINENAME_entry.get()
    LOTNO = LOTNO_entry.get()
    ISSUEDATE = ISSUEDATE_entry.get()
    EXPDATE = EXPDATE_entry.get()
    DOSAGE = DOSAGE_entry.get()
    PRICE = PRICE_entry.get()
    PRODUCTQT = PRODUCTQT_entry.get()

    # Validate required fields
    if REFRENCENO == "" or MEDICINENAME == "" or MEDICINETYPE == "":
        MessageBox.showinfo("ALERT", "Please enter fields you want to update!")
    else:
        try:
            con = connect_db()
            cursor = con.cursor()
            query = "UPDATE pharmacy SET MEDICINETYPE = %s, MEDICINENAME = %s, LOTNO = %s, ISSUEDATE = %s, EXPDATE = %s, DOSAGE = %s, PRICE = %s, PRODUCTQT = %s WHERE REFRENCENO = %s"
            values = (MEDICINETYPE, MEDICINENAME, LOTNO, ISSUEDATE, EXPDATE, DOSAGE, PRICE, PRODUCTQT, REFRENCENO)
            cursor.execute(query, values)
            con.commit()
            cursor.close()
            con.close()
            MessageBox.showinfo("Status", "Successfully Updated")
            # Clear input fields after successful update
            reset_fields()
            fetch_data()
        except Exception as e:
            MessageBox.showerror("Error", f"Error updating database: {str(e)}")

# Delete function
def Del():
    REFRENCENO = REFRENCENO_entry.get()
    
    if REFRENCENO == "":
        MessageBox.showinfo("ALERT", "Please enter Reference Number to delete row")
    else:
        try:
            con = connect_db()
            cursor = con.cursor()
            query = "DELETE FROM pharmacy WHERE REFRENCENO = %s"
            cursor.execute(query, (REFRENCENO,))
            con.commit()
            cursor.close()
            con.close()
            reset_fields()
            fetch_data()
            MessageBox.showinfo("Status", "Successfully Deleted")
        except Exception as e:
            MessageBox.showerror("Error", f"Error deleting from database: {str(e)}")
def reset_fields():
    REFRENCENO_entry.delete(0, 'end')
    MEDICINETYPE_entry.delete(0, 'end')
    MEDICINENAME_entry.delete(0, 'end')
    LOTNO_entry.delete(0, 'end')
    ISSUEDATE_entry.delete(0, 'end')
    EXPDATE_entry.delete(0, 'end')
    DOSAGE_entry.delete(0, 'end')
    PRICE_entry.delete(0, 'end')
    PRODUCTQT_entry.delete(0, 'end')

# Show all function
def show_all():
    fetch_data()

# Set function
def set_fields():
    selected = pharmacy_table.focus()
    values = pharmacy_table.item(selected, 'values')
    if values:
        reset_fields()
        REFRENCENO_entry.insert(0, values[0])
        MEDICINETYPE_entry.insert(0, values[1])
        MEDICINENAME_entry.insert(0, values[2])
        LOTNO_entry.insert(0, values[3])
        ISSUEDATE_entry.insert(0, values[4])
        EXPDATE_entry.insert(0, values[5])
        DOSAGE_entry.insert(0, values[6])
        PRICE_entry.insert(0, values[7])
        PRODUCTQT_entry.insert(0, values[8])
    else:
        MessageBox.showinfo("ALERT", "Please select a row to set fields")

# Search function
def search():
    search_by = search_Combo.get()
    search_txt = txtsearch.get()

    if search_txt == "":
        MessageBox.showinfo("ALERT", "Please enter a value to search")
    else:
        try:
            con = connect_db()
            cursor = con.cursor()
            if search_by == "Refrence":
                query = "SELECT * FROM pharmacy WHERE REFRENCENO LIKE %s"
            elif search_by == "Medicine":
                query = "SELECT * FROM pharmacy WHERE MEDICINENAME LIKE %s"
            elif search_by == "Lot":
                query = "SELECT * FROM pharmacy WHERE LOTNO LIKE %s"
            
            cursor.execute(query, ('%' + search_txt + '%',))
            rows = cursor.fetchall()
            rows = cursor.fetchall()
            # Clear previous entries in fields
            reset_fields()

            for row in rows:
                REFRENCENO_entry.insert(0, row[0])
                MEDICINETYPE_entry.insert(0, row[1])
                MEDICINENAME_entry.insert(0, row[2])
                LOTNO_entry.insert(0, row[3])
                ISSUEDATE_entry.insert(0, row[4])
                EXPDATE_entry.insert(0, row[5])
                DOSAGE_entry.insert(0, row[6])
                PRICE_entry.insert(0, row[7])
                PRODUCTQT_entry.insert(0, row[8])
            
            cursor.close()
            con.close()
        except Exception as e:
            MessageBox.showerror("Error", f"Error searching database: {str(e)}")



win=Tk()
win.geometry("2400x1100+0+0")
win.title("Pharmacy Management System")
  
pharmacy=Label (win,text="PHARMACY MANAGEMENT SYSTEM", bd=10,fg="dark green", bg= "white", relief="sunken",font=("times of roman",20, "bold "))
pharmacy.grid(ipadx=600,ipady=20)
      
  #==================================DATAFRAME=============================================================      
        
DataFrame=Frame(win,bd=15, relief=RIDGE,padx=0) 
DataFrame.place(x=10,y=95,width=1510,height=380)  
DataFrameLeft= LabelFrame(DataFrame,bd=10,relief=RIDGE,padx=20,text="MEDICINE INFORMATION",fg="darkgreen",font=("times new roman",15,"bold"))
DataFrameLeft.place(x=10,y=15,width=900,height=350)  
DataFrameRight= LabelFrame(DataFrame,bd=10,relief=RIDGE,padx=20,text="MEDICINE ADD DEPARTMENT",fg="darkgreen",font=("times new roman",15,"bold"))
DataFrameRight.place(x=920,y=15,width=560,height=320)      
  #===================================BUTTON FRAME=================================================  
ButtonFrame=Frame(win,bd=15, relief=RIDGE,padx=0) 
ButtonFrame.place(x=10,y=465,width=1510,height=65)     
  #=====================================MAIN BUTTON================================================    
btnAddData=Button(ButtonFrame,text="MEDICINEADD",command=Insert, font=("times new roman",15,"bold"),width=14,fg="darkgreen",bg="white")
btnAddData.grid(row=0,column=0)

btnAddData=Button(ButtonFrame,text="UPDATE",command=Update, font=("times new roman",15,"bold"),width=12,fg="darkgreen",bg="white")
btnAddData.grid(row=0,column=1)

btnAddData=Button(ButtonFrame,text="DELETE",command=Del, font=("times new roman",15,"bold"),width=10,fg="white",bg="red")
btnAddData.grid(row=0,column=2)

btnAddData=Button(ButtonFrame,text="RESET",font=("times new roman",15,"bold"),width=10,fg="darkgreen",bg="white")
btnAddData.grid(row=0,column=3)

btnAddData=Button(ButtonFrame,text="SET",font=("times new roman",15,"bold"),width=10,fg="darkgreen",bg="white")
btnAddData.grid(row=0,column=4)

#====================================SEARCH BY===================================================
lblsearch=Label(ButtonFrame,font=("times new roman",17,"bold"),fg="white",bg="red",text="SEARCH BY",padx=2)
lblsearch.grid(row=0,column=5)    
            
search_Combo=ttk.Combobox(ButtonFrame,width=8,font=("times new roman",17,"bold"),state="readonly")
search_Combo["values"]=("Refrence","Medicince","LOt")
search_Combo.grid(row=0,column=6)
search_Combo.current(0)

txtsearch=Entry(ButtonFrame,bd=3,relief=RIDGE,width=12,font=("arial",17,"bold"))
txtsearch.grid(row=0,column=7)
searchBtn=Button(ButtonFrame,text="SEARCH",font=("times new roman",17,"bold"),width=9,fg="darkgreen",bg="white")
searchBtn.grid(row=0,column=8)

searchBtn=Button(ButtonFrame,text="SHOW ALL",font=("times new roman",17,"bold"),width=9,fg="darkgreen",bg="white")
searchBtn.grid(row=0,column=9)
#====================================LABEL AND ENTRY==============================================
REFRENCENO=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="REFERENCE NO",padx=2)
REFRENCENO.grid(row=0,column=0)  
REFRENCENO_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
REFRENCENO_entry.grid(row=0,column=1)
#ref_Combo=ttk.Combobox(DataFrameLeft,width=30,font=("times new roman",10,"bold"),state="readonly")
#ref_Combo["values"]=("Refrence","Medicince","LOt")
#ref_Combo.grid(row=0,column=1)
#ref_Combo.current(0)

Medicinetype=Label(DataFrameLeft,width=30,font=("times new roman",12,"bold"),text="MEDICINE TYPE",padx=2)
Medicinetype.grid(row=1,column=0)  
#Medicinetype_Combo=ttk.Combobox(DataFrameLeft,width=30,font=("times new roman",10,"bold"),state="readonly")
#Medicinetype_Combo["values"]=("tablets","liquid","capsules","Drops","injection","inhaler")
#Medicinetype_Combo.grid(row=1,column=1)
#Medicinetype_Combo.current(0)
MEDICINETYPE_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
MEDICINETYPE_entry.grid(row=1,column=1)

MEDICINENAME=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="MEDICINE NAME",padx=2)
MEDICINENAME.grid(row=2,column=0) 
MEDICINENAME_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
MEDICINENAME_entry.grid(row=2,column=1)
#Medicinename_Combo=ttk.Combobox(DataFrameLeft,width=30,font=("times new roman",10,"bold"),state="readonly")
#Medicinename_Combo["values"]=("ASPIRIN","PARCETAMOL","IBRUPROFEN","VITAMIN D","DPIs(DRYPOWEDER INHALER)","COFSILS","ALOGLIPTIN","GLICAZIDE","VICKS","LIMCEE","GLUCOSE")
#Medicinename_Combo.grid(row=2,column=1)
#Medicinename_Combo.current(0)

LOTNO=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="LOT NO",padx=2)
LOTNO.grid(row=3,column=0)
LOTNO_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
LOTNO_entry.grid(row=3,column=1)

ISSUEDATE=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="ISSUE DATE",padx=2)
ISSUEDATE.grid(row=4,column=0) 
ISSUEDATE_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
ISSUEDATE_entry.grid(row=4,column=1)


EXPDATE=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="EXP DATE",padx=2)
EXPDATE.grid(row=5,column=0) 
EXPDATE_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
EXPDATE_entry.grid(row=5,column=1)

DOSAGE=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="DOSAGE",padx=2)
DOSAGE.grid(row=6,column=0) 
DOSAGE_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
DOSAGE_entry.grid(row=6,column=1)

PRICE=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="PRICE",padx=2)
PRICE.grid(row=7,column=0) 
PRICE_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
PRICE_entry.grid(row=7,column=1)

PRODUCTQT=Label(DataFrameLeft,font=("times new roman",12,"bold"),text="PRODUCT QT",padx=2)
PRODUCTQT.grid(row=8,column=0) 
PRODUCTQT_entry=Entry(DataFrameLeft,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=29)
PRODUCTQT_entry.grid(row=8,column=1)
#======================================IMAGE=============================================================


lblrefno=Label(DataFrameRight,font=("times new roman",12,"bold"),text="REFERENCE NO",padx=2)
lblrefno.place(x=0,y=80)
txtrefNo=Entry(DataFrameRight,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=14)
txtrefNo.place(x=135,y=80)

lblmedName=Label(DataFrameRight,font=("times new roman",12,"bold"),text="MEDICINE NAME",padx=2)
lblmedName.place(x=0,y=110)
txtmedName=Entry(DataFrameRight,font=("times new roman",12,"bold"),bg="white",bd=2,relief=RIDGE,width=14)
txtmedName.place(x=135,y=110)

#========================================SIDE FRAME========================================================
side_frame=Frame(DataFrameRight,bd=4,relief=RIDGE,bg="white")
side_frame.place(x=0,y=150,width=300,height=130)

sc_x=ttk.Scrollbar(side_frame,orient=HORIZONTAL)
sc_x.pack(side=BOTTOM,fill=X)
sc_Y=ttk.Scrollbar(side_frame,orient=VERTICAL)
sc_Y.pack(side=RIGHT,fill=Y)

medicine_table=ttk.Treeview(side_frame,column=("ref","medname"),xscrollcommand=sc_x.set,)
sc_x.config(command=medicine_table.xview)
medicine_table.heading("ref",text="reference")
medicine_table.heading("medname",text="medicince name")
medicine_table["show"]="headings"
medicine_table.pack(fill=BOTH,expand=1 )

medicine_table.column("ref",width=100)
medicine_table.column("medname",width=100)

#=====================================MEDICINE ADD BUTTONS============================================
down_frame=Frame(DataFrameRight,bg="white",bd=2,relief=RIDGE,width=29)
down_frame.place(x=330,y=150,width=115,height=120)
btnAddmed=Button(down_frame,text="ADD",font=("times new roman",12,"bold"),width=13,fg="darkgreen",bg="yellow",pady=4)
btnAddmed.grid(row=0,column=0)

btnAddmed=Button(down_frame,text="DELETE",font=("times new roman",12,"bold"),width=13,fg="darkgreen",bg="red",pady=4)
btnAddmed.grid(row=1,column=0)

btnAddmed=Button(down_frame,text="UPDATE",font=("times new roman",12,"bold"),width=13,fg="white",bg="blue",pady=4)
btnAddmed.grid(row=2,column=0)
#==========================================frame details===============================================
Framedetails=Frame(win,bd=15,relief=RIDGE)
Framedetails.place(x=10,y=540,width=1510,height=380)
#======================================MAIN TABLE & SCROLL BAR=========================================
Table_frame=Frame(win,bd=15,relief=RIDGE)
Table_frame.place(x=30,y=560,width=1470,height=270)

scroll_X=ttk.Scrollbar(Table_frame,orient=HORIZONTAL)
scroll_X.pack(side=BOTTOM,fill=X)
scroll_Y=ttk.Scrollbar(side_frame,orient=VERTICAL)
scroll_Y.pack(side=RIGHT,fill=Y)

pharmacy_table=ttk.Treeview(Table_frame,column=("ref","Medicinetype","Medicine name","LotNo","Issuedate","Expdate","Doasge","PRICE","ProductQt"))
scroll_X.pack(side=BOTTOM,fill=X)
scroll_Y.pack(side=RIGHT,fill=Y)

pharmacy_table["show"]="headings"

pharmacy_table.heading("ref",text="REFERENCE NO")
pharmacy_table.heading("Medicinetype",text="MEDICINE TYPE")
pharmacy_table.heading("Medicine name",text="MEDICINE NAME")
pharmacy_table.heading("LotNo",text="LOT NO")
pharmacy_table.heading("Issuedate",text="ISSUE DATE")
pharmacy_table.heading("Expdate",text="EXP DATE")
pharmacy_table.heading("Doasge",text="DOSAGE")
pharmacy_table.heading("PRICE",text="PRICE")
pharmacy_table.heading("ProductQt",text="PRODUCT QT")

pharmacy_table.pack(fill=BOTH,expand=1)

pharmacy_table.column("ref",width=90)
pharmacy_table.column("Medicinetype",width=90)
pharmacy_table.column("Medicine name",width=90)
pharmacy_table.column("LotNo",width=90)
pharmacy_table.column("Issuedate",width=100)
pharmacy_table.column("Expdate",width=100)

pharmacy_table.column("Doasge",width=100)
pharmacy_table.column("PRICE",width=100)
pharmacy_table.column("ProductQt",width=100)

#=======================================ADD MEDICINE FUNCTINALITY DECLARATION===============================




win.mainloop()