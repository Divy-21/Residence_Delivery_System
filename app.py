from flask import Flask, request, render_template, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Serve the login page
@app.route('/')
def login_page():
    return render_template('delivery_system.html')
   

# Define the /login endpoint
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username'] 
    password = request.form['password']
    
    # Here you can add your authentication logic
    if username == 'admin' and password == 'password':
        return redirect(url_for('lot'))
    else:
        return 'Invalid username or password'
    
@app.route('/lot')
def lot():
    return render_template('lot_system.html')
    

@app.route('/search')    
def search():
    l = 2
    res = ['Lister','Plh','Nipsy']
    fname = ['Akshat','Noel','IDK']
    lname = ['C','j',"Diddy"]
    room = [357,120,122]
    ccid = ['akshatcd','noeljddc','pdiddycc']
    return render_template('search.html',res=res,fname=fname,lname=lname,room=room,l=l,ccid=ccid)

def init_db():
    conn = sqlite3.connect('names.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS names (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   name TEXT NOT NULL)''')
    cursor.execute('''
        INSERT INTO names (name) VALUES 
        ('John Doe'),
        ('Jane Smith'),
        ('Alice Johnson'),
        ('Bob Brown')''')
    conn.commit()
    cursor.close()
    conn.close()


if __name__ == '__main__':
    app.run(debug=True,port=5001)
