from datetime import date
import sqlite3
import os

if not os.path.exists('databases'):
    os.makedirs('databases')

# Connect to SQLite (Creates a file-based database)
with open('data/residences.txt', 'r') as f:
    mydata = f.readline().strip()
    mydata = mydata.split(",")
for j in mydata:
    print(j,mydata)
    mycon = sqlite3.connect(f"databases/{j}.db")
    mycon.close()


signedin=True
def return_records(results):
    length=len(results)
    ccid=[i[0] for i in results]
    lastname=[i[1] for i in results]
    firstname=[i[2] for i in results ]
    residence=[i[3] for i in results]
    room=[i[4] for i in results]
    return length,ccid,lastname,firstname,residence,room 



while signedin:
    today_date=date.today()
    int_today_date=int(''.join(str(today_date).split('-')))
    mycon=sqlite3.connect('warehouse.db')
    mycursor = mycon.cursor()
    table_name=f"warehouse{str(int_today_date)}"
    mycursor.execute(f'''
CREATE TABLE IF NOT EXISTS {table_name} (
    sr_no INTEGER PRIMARY KEY AUTOINCREMENT,
    ccid TEXT NOT NULL,
    lastname TEXT NOT NULL,
    firstname TEXT NOT NULL,
    residence TEXT NOT NULL,
    roomnumber INTEGER NOT NULL,
    date DATE NOT NULL,
    lot_no INTEGER NOT NULL,
    QR_info INTEGER
);
''')
    lot_no=1

    
    create_lot=True
    while create_lot:
        data={}
        valid_input=False
        while not valid_input:
            last_firstname = input("Enter the name on the package (lastname, firstname): ")
            name = last_firstname.split(",")
            if len(name) != 2:
                print("Invalid input. Please enter in 'lastname, firstname' format.")
                valid_input=False
            else:
                valid_input=True
                lastname = name[0].strip()
                firstname = name[1].strip()
                print(firstname,lastname)
        query=f"SELECT * FROM studentrecords WHERE lastname='{lastname}' AND firstname='{firstname}';"
        mycursor.execute(query)
        
        results = mycursor.fetchall()
        list_variables=return_records(results)
        print(results)
        ccid=results[0][0] # get code from divy
        for i in range(len(results)):
            if results[i][0]==ccid:
                c_data=results[i]
        
        query=f"INSERT INTO {table_name} (ccid,lastname,firstname,residence,roomnumber,date,lot_no) VALUES('{c_data[0]}','{c_data[1]}','{c_data[2]}','{c_data[3]}',{c_data[4]},'{today_date}',{lot_no});"
        mycursor.execute(query)
        mycon.commit()
        mycursor.execute(f"select sr_no from {table_name} where ccid='{ccid}';")
        sr_no=mycursor.fetchone()
        sr_no=sr_no[0]
        QR_info = int(f"{sr_no}{int_today_date}{lot_no}")
        
        print(c_data)

        query=f"UPDATE {table_name} SET QR_info={QR_info} where sr_no={sr_no} AND ccid='{ccid}';"
        mycursor.execute(query)
        mycon.commit()
        print('Record updated')
        ans=input('next (y/n)?')
        if ans!='y':
            create_lot=False
            lot_no+=1
            mycursor.execute(f"select * from {table_name};")
            records=mycursor.fetchall()
            for i in records:
                if i[4] in data.keys():
                    data[i[4]].append(i)
                else:
                    data[i[4]]=[i]
    mycon.close()
    print(data)
    for i in data.keys():
        table_name_r=f"{i}{str(int_today_date)}"
        mycon = sqlite3.connect(f"databases/{i}.db")
        mycursor = mycon.cursor()
        mycursor.execute(f'''
CREATE TABLE IF NOT EXISTS '{table_name_r}' (
        sr_no INTEGER,
        ccid TEXT NOT NULL,
        lastname TEXT NOT NULL,
        firstname TEXT NOT NULL,
        residence TEXT NOT NULL,
        roomnumber INTEGER NOT NULL,
        date DATE NOT NULL,
        lot_no INTEGER NOT NULL,
        QR_info INTEGER
);
''')   
        
        for j in data[i]:
            print(table_name_r)
            print(f"{j[0]},'{j[1]}','{j[2]}','{j[3]}','{j[4]}',{j[5]},'{j[6]}',{j[7]},{j[8]}")
            query=f"INSERT INTO '{table_name_r}' (sr_no,ccid,lastname,firstname,residence,roomnumber,date,lot_no,QR_info) VALUES({j[0]},'{j[1]}','{j[2]}','{j[3]}','{j[4]}',{j[5]},'{j[6]}',{j[7]},{j[8]});"
            mycursor.execute(query)
            mycon.commit()
        mycon.close()
    signedin=False
    print('All records updated')
