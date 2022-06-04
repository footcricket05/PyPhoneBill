import mysql.connector as mq

def menu():
    print("\t\t\t ONLINE TELEPHONE BILLING SYSTEM")
    print("\t\t\t ===============================\n")
    print("\t\t\t\t MAIN MENU")
    print("\t\t\t\t =========\n")
    print("\t\t1. Register User \t 2. Search customer \n")
    print("\t\t3. Update Customer \t 4. Generate Bill \n")
    print("\t\t5. Delete Customer \t 6. Display records \n")
    print("\t\t7. Help            \t 8. Exit \n")

def register():
    print("\n\t\t\tNew Customer Registration.....")
    print("\t\t\t==============================\n")
    print("Details of the customer are phone_no, name, address, aadhar_no respectively:")
    ph=input("Enter your Phone number:")
    n=input("Enter your Name:")
    add=input("Enter your Address:")
    adh=input("Enter your 12-digit Aadhar Card number:")
    con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
    cur=con.cursor()
    query="insert into customer(Phno,name,address,aadhar_no,ftp)values({},'{}','{}','{}',{})".format(ph,n,add,adh,0)
    cur.execute(query)
    con.commit()
    print("\nSuccessfully Registered the user.....")
    con.close()

def search():
    print("\n\t\t\tSearch Customer.....")
    print("\t\t\t====================\n")
    print("Details of the customer are phone_no, name, address, aadhar_no, bill,status(paid or unpaid), first time payer(yes:0/no:1) respectively:")
    ph=input("\nEnter your phone number:")
    con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
    cur=con.cursor()
    query="select * from customer where Phno={}".format(ph)
    cur.execute(query)
    res=cur.fetchall()
    if res==[]:
        print("Customer does not exist.....")
    else:
        print(res)
    con.close()
 
def modify():
    print("\n\t\t\tUpdate Customer Data.....")
    print("\t\t\t=========================\n")
    ph=input("\nEnter your phone number:")
    con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
    cur=con.cursor()
    query="select * from customer where Phno={}".format(ph)
    cur.execute(query)
    res=cur.fetchall()
    if res==[]:
        print("Customer does not exist.....")
    else:
        print("1. Name\n2. Address\n3. Aadhar_no")
        ch=int(input("Enter choice to update:"))
        if ch==1:
            n=input("Enter new name:")
            query="update customer set name='{}' where phno={}".format(n,ph)
            cur.execute(query)
            con.commit()
            print("Successfully updated name.....")
        elif ch==2:
            add=input("Enter new address:")
            query="update customer set address='{}' where phno={}".format(add,ph)
            cur.execute(query)
            con.commit()
            print("Successfully updated address.....")
        elif ch==3:
            adr=input("Enter new aadhar_no:")
            query="update customer set aadhar_no='{}' where phno={}".format(adr,ph)
            cur.execute(query)
            con.commit()
            print("Successfully updated aadhar_no.....")
        else:
            print("Please choose the correct choice.....")
    con.close()
            
def billing():
    print("\t\t\tBilling.....")
    print("\t\t\t============\n")
    ph=input("\nEnter your phone number:")
    con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
    cur=con.cursor()
    query="select * from customer where phno={}".format(ph)
    cur.execute(query)
    res=cur.fetchall()
    if res==[]:
        print("Customer does not exist.....")
    else:
        calls=int(input("Enter number of calls:"))
        bill=0
        finalbill=0
        ftime=0
        next50to100_=0
        next100to150_=0
        over150_=0
        if res[0][6]==0:    
            ftime=0
            if calls>150:
                bill=bill+(calls-150)*3 + 50*2 + 50*1
                next50to100_=50
                next100to150_=100
                over150_=(calls-150)*3

            elif 100<calls<=150:
                bill=bill+(calls-100)*2 + 50*1
                next100to150_=(calls-100)*2 
                next50to100_=50

            elif 50<calls<100:
                bill=bill+(calls-50)*1
                next50to100_=(calls-50)*1

        elif res[0][6]==1:
            ftime=1
            if calls>150:
                bill=bill+(calls)*3
                over150_=calls*3

            elif 100<calls<150:
                bill=bill+(calls)*2
                next100to150_=calls*2

            elif calls<100:
                bill=bill+(calls)*1
                next50to100_=calls*1

        print("\t\t\tBilling.....")
        print("\t\t\t============\n")
        old_bill=res[0][4]
        if res[0][5]!="Paid":
            print("\n\t\tPending bill amount:",old_bill)
            if ftime==0:
                print("\n\t\tFirst 50 free calls:",0)
                print("\n\t\tNext 51-100 calls@1.0Rs/call:",next50to100_)
                print("\n\t\tNext 100-150 calls@2.0Rs/call:",next100to150_)
                print("\n\t\tNext over 150 calls@3.0Rs/call:",over150_)
            else:
                print("\n\t\tTotal calls",calls)
                if calls>150:
                    print("\n\t\tover 150 calls is Rs3.0/call =",over150_)    
                elif 100<calls<150:
                    print("\n\t\tbetween 150-100 calls is Rs2.0/call =",next100to150_)
                else:
                    print("\n\t\tbelow 100 calls is Rs1.0/call =",next50to100_)
                
            print("\n\t\tNew bill amount:    ",bill)
            print("\n\t\t========================")
            finalbill=old_bill+bill
            print("\t\tTotal amount to pay:  ",finalbill)
            
        else:
            print("\n\t\tLast paid bill amount",old_bill)
            print("\n\t\tTotal calls",calls)
            if calls>150:
                print("\n\t\tover 150 calls is Rs3.0/call =",over150_)
            elif 100<calls<150:
                print("\n\t\tbetween 150-100 calls is Rs2.0/call =",next100to150_)
            else:
                print("\n\t\tbelow 100 calls is Rs1.0/call =",next50to100_)

            print("\n\t\tNew bill amount:    ",bill)
            print("\n\t\t========================")
            finalbill=bill
            print("\t\tTotal bill amount:  ",finalbill)
        
        print("\t\t========================")
        ch=input("\nPress Y to pay the bill now or any other key to pay later:")
        if ch in ['Y','y','yes','Yes']:
            if ftime==0:
                query="update customer set bill='{}',status='Paid',ftp=1 where phno={}".format(finalbill,ph)
            else:
                query="update customer set bill='{}',status='Paid' where phno={}".format(finalbill,ph)
            cur.execute(query)
            con.commit()
            print("Successfully paid the bill.....")

        else:
            query="update customer set bill='{}',status='Unpaid',ftp=1 where phno={}".format(finalbill,ph)
            cur.execute(query)
            con.commit()
            print("Please make payment as soon as possible.....")
    con.close()

def remove():
    ph=input("\nEnter your phone number:")
    con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
    cur=con.cursor()
    query="select * from customer where phno={}".format(ph)
    cur.execute(query)
    res=cur.fetchall()
    if res==[]:
        print("Customer does not exist.....")
    else:
        ch=input("Are you sure to delete the customer.....Yes/No:")
        if ch in ['Y', 'y','yes', 'Yes']: 
            query="delete from customer where Phno={}".format(ph)
            cur.execute(query)
            con.commit()
            print("Successfully deleted from database.....")
        else:
            print("No changes made in the databse")
    con.close()
def display():
  con=mq.connect(host="localhost",user="root",password="Calvin@0203",database="telephone")
  cur=con.cursor()
  query="select * from customer"
  cur.execute(query)
  res=cur.fetchall()
  con.commit()
  fh=open('tele_file.txt','w+')
  for eachrecord in res:
    strformat=str(eachrecord)
    fh.write(strformat)                 
    fh.write('\n')
    fh.flush()
  fh.close

  fh=open('tele_file.txt',"r")
  readr=fh.read()
  print(readr)
  fh.close()
  con.close()
  
def helping():
    print("\t\t\tHelp")
    print("\t\t\t====")
    print("First 50 calls are free")
    print("51-100 calls are 1.0 Rs per call")
    print("101-150 calls are 2.0 Rs per call")
    print("Above 150 calls are 3.0 Rs per call")
    
while True:
    menu()
    ch=int(input("Enter your choice:"))
    if ch==1:
        register()
    elif ch==2:
        search()
    elif ch==3:
        modify()
    elif ch==4:
        billing()
    elif ch==5:
        remove()
    elif ch==6:
        display()         
    elif ch==7:
        helping()
    elif ch==8:
        exit()
    else:
        print("Please choose the correct choice and try again")
        
    ch=input("\n\nPress y to continue and any other key to exit:")
    if ch not in ["Y","y","yes","Yes"]:
        break
