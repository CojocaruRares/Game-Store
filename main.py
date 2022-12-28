from flask import Flask, render_template, url_for, request, redirect
import cx_Oracle
from datetime import datetime

app = Flask(__name__)

#connect to the database using cx_Oracle
cx_Oracle.init_oracle_client(lib_dir= r"C:\app\Rares\product\21c\dbhomeXE\bin")
con = cx_Oracle.connect("SYSTEM","kingnr1", "localhost/xe")

#Our database has 6 tables:
#-VideoGames
#-Category  } -> these tables offer aditional information for VideoGame products
#-Developer }    a developer can have more products, so 1:n relation
#-Clients
#-ContactInfo -> 1:1 relation with Clients
#-Transaction -> 1:n relation with Clients and VideoGames (a product/client can be in more than one transaction)

@app.route('/')
@app.route('/VideoGames')
def VideoGames():
    games = []
    cur = con.cursor()
    cur2 = con.cursor()
    cur.execute('select * from videogames')
    for result in cur:
        game = {}
        game['product_id'] = result[0]
        game['product_name'] = result[1]
        game['price'] = result[2]
        cur2.execute('select developer_name from developer where developer_id = :ID', ID = result[3])
        for result2 in cur2:
            game['developer'] = result2[0]
        games.append(game)
        cur2.execute('select genre, platform from category where category_id = :ID ', ID=result[4])
        for result2 in cur2:
            game['genre'] = result2[0]
            game['platform'] = result2[1]
    cur2.close()
    cur.close()
    return render_template('VideoGames.html', games= games)

@app.route('/addVideoGame',methods = ["GET","POST"])
def addVideoGame():
    if request.method == 'POST':
        values = []
        values.append("'" + request.form['name'] + "'")
        values.append("'" + request.form['price'] + "'")
        values.append("'" + request.form['Category_ID'] + "'")
        values.append("'" + request.form['Developer_ID'] + "'")

        fields = ['product_name','price','developer_developer_id','category_category_id']
        cur = con.cursor()
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % ('videogames', ', '.join(fields), ', '.join(values))
        cur.execute(sql)
        cur.execute('commit')
        cur.close()
        return redirect('/VideoGames')
    else:
        return render_template('addVideoGame.html')

@app.route('/delVideoGame',methods = ["GET","POST"])
def delVideoGame():
    if request.method == 'POST':
        Product_ID = request.form.get('Product_ID')
        cur = con.cursor()
        cur.execute('delete from videogames where product_id = :ID', ID=Product_ID)
        cur.execute('commit')
        cur.close()
        return redirect('/VideoGames')
    else:
        return render_template("delVideoGame.html")

@app.route('/updateVideoGame',methods = ["GET","POST"])
def updateVideoGame():
    if request.method == 'POST':
        Product_ID = request.form.get('Product_ID')
        name = request.form.get('name')
        price = request.form.get('price')
        D_ID = request.form.get('Developer_ID')
        C_ID = request.form.get('Category_ID')
        cur = con.cursor()
        if name != '':
            cur.execute('update videogames set product_name = :n where product_id = :ID', n=name, ID=Product_ID)
        if price != '':
            cur.execute('update videogames set price = :p where product_id = :ID', p=price, ID=Product_ID)
        if D_ID != '':
            cur.execute('update videogames set developer_developer_id = :d where product_id = :ID', d=D_ID, ID=Product_ID)
        if C_ID != '':
            cur.execute('update videogames set category_category_id = :c where product_id = :ID', c=C_ID, ID=Product_ID)
        cur.execute('commit')
        cur.close
        return redirect('/VideoGames')
    else:
        return render_template('updateVideoGame.html')


@app.route('/Categories')
def Categories():
    categories = []
    cur = con.cursor()
    cur.execute('select * from category')
    for result in cur:
        category = {}
        category['category_id'] = result[0]
        category['genre'] = result[1]
        category['platform'] = result[2]
        categories.append(category)
    cur.close()
    return render_template('Categories.html', categories= categories)

@app.route('/addCategory',methods = ["GET","POST"])
def addCategory():
    if request.method == 'POST':
        values = []
        values.append("'" + request.form['genre'] + "'")
        values.append("'" + request.form['platform'] + "'")
        fields = ['genre','platform']
        cur = con.cursor()
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % ('category', ', '.join(fields), ', '.join(values))
        cur.execute(sql)
        cur.execute('commit')
        cur.close()
        return redirect('/Categories')
    else:
        return render_template('addCategory.html')

@app.route('/delCategory',methods = ["GET","POST"])
def delCategory():
    if request.method == 'POST':
        Category_ID = request.form.get('Category_ID')
        cur = con.cursor()
        cur.execute('delete from category where category_id = :ID', ID=Category_ID)
        cur.execute('commit')
        cur.close()
        return redirect('/Categories')
    else:
        return render_template("delCategory.html")

@app.route('/updateCategory',methods = ["GET","POST"])
def updateCategory():
    if request.method == 'POST':
        Category_ID = request.form.get('Category_ID')
        genre = request.form.get('genre')
        platform = request.form.get('platform')
        cur = con.cursor()
        cur.execute('update category set genre = :genre, platform = :platform where category_id = :ID', genre=genre, platform = platform, ID=Category_ID)
        cur.execute('commit')
        cur.close
        return redirect('/Categories')
    else:
        return render_template('updateCategory.html')


@app.route('/Developers')
def Developers():
    developers = []
    cur = con.cursor()
    cur.execute('select * from developer')
    for result in cur:
        developer = {}
        developer['developer_id'] = result[0]
        developer['developer_name'] = result[1]
        developers.append(developer)
    cur.close()
    return render_template('Developers.html', developers= developers)


@app.route('/addDeveloper',methods = ["GET","POST"])
def addDeveloper():
    if request.method == 'POST':
        developer_name = request.form.get('name')
        cur = con.cursor()
        cur.execute('insert into developer (developer_name) values(:name)',name = developer_name)
        cur.execute('commit')
        cur.close()
        return redirect('/Developers')
    else:
        return render_template('addDeveloper.html')

@app.route('/delDeveloper',methods = ["GET","POST"])
def delDeveloper():
    if request.method == 'POST':
        Developer_ID = request.form.get('Developer_ID')
        cur = con.cursor()
        cur.execute('delete from developer where developer_id = :ID', ID=Developer_ID)
        cur.execute('commit')
        cur.close()
        return redirect('/Developers')
    else:
        return render_template("delDeveloper.html")

@app.route('/updateDeveloper',methods = ["GET","POST"])
def updateDeveloper():
    if request.method == 'POST':
        Developer_ID = request.form.get('Developer_ID')
        name = request.form.get('name')
        cur = con.cursor()
        cur.execute('update developer set developer_name = :n where developer_id = :ID', n=name, ID=Developer_ID)
        cur.execute('commit')
        cur.close
        return redirect('/Developers')
    else:
        return render_template('updateDeveloper.html')

@app.route('/Clients')
def Clients():
    clients = []
    cur = con.cursor()
    cur2 = con.cursor()
    cur.execute('select * from clients')
    for result in cur:
        client = {}
        client['client_id'] = result[0]
        client['first_name'] = result[1]
        client['last_name'] = result[2]
        client['wallet'] = result [3]

        cur2.execute('select email, phone from contactinfo where clients_client_id = :ID', ID= result[0])
        for result2 in cur2:
            client['email'] = result2[0]
            client['phone'] = result2[1]
        clients.append(client)
    cur2.close()
    cur.close()
    return render_template("Clients.html", clients= clients)

@app.route('/addClient',methods = ["GET","POST"])
def addClient():
    if request.method == 'POST':
        values = []
        values.append("'" + request.form['f_name'] + "'")
        values.append("'" + request.form['l_name'] + "'")
        values.append("'" + request.form['wallet'] + "'")
        fields = ['first_name', 'last_name', 'wallet']
        cur = con.cursor()
        cur.execute("select last_number from user_sequences where sequence_name = 'CLIENTS_CLIENT_ID_SEQ'")
        for result in cur:
            client_id = result[0]
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % ('clients', ', '.join(fields), ', '.join(values))
        cur.execute(sql)
        values.clear()
        fields.clear()
        values.append("'" + str(client_id) + "'")
        values.append("'" + request.form['email'] + "'")
        values.append("'" + request.form['phone'] + "'")
        fields = ['Clients_client_id','email', 'phone']
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % ('contactinfo', ', '.join(fields), ', '.join(values))
        cur.execute(sql)
        cur.execute('commit')
        cur.close()
        return redirect('/Clients')
    else:
        return render_template('addClient.html')

@app.route('/delClient', methods = ["GET", "POST"])
def delClient():
    if request.method == 'POST':
        Client_ID = request.form.get('Client_ID')
        cur = con.cursor()
        cur.execute('delete from transactions where clients_client_id = :ID', ID=Client_ID)
        cur.execute('delete from contactinfo where clients_client_id = :ID', ID=Client_ID)
        cur.execute('delete from clients where client_id = :ID', ID=Client_ID)
        cur.execute('commit')
        cur.close()
        return redirect('/Clients')
    else:
        return render_template("delClient.html")

@app.route('/updateClient', methods = ["GET", "POST"])
def updateClient():
    if request.method == 'POST':
        Client_ID = request.form.get('Client_ID')
        f_name = request.form.get('f_name')
        l_name = request.form.get('l_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        wallet = request.form.get('wallet')
        cur = con.cursor()
        if f_name != '':
            cur.execute('update clients set first_name = :fname where client_id = :ID', fname=f_name, ID=Client_ID)
        if l_name != '':
            cur.execute('update clients set last_name = :lname where client_id = :ID', lname=l_name, ID=Client_ID)
        if email != '':
            cur.execute('update contactinfo set email = :mail where clients_client_id = :ID', mail=email, ID=Client_ID)
        if phone != '':
            cur.execute('update contactinfo set phone = :p where clients_client_id = :ID', p=phone, ID=Client_ID)
        if wallet != '':
            cur.execute('update clients set wallet = :w where client_id = :ID', w=wallet, ID=Client_ID)
        cur.execute('commit')
        cur.close
        return redirect('/Clients')
    else:
        return render_template('updateClient.html')

@app.route('/Transactions')
def Transactions():
    transactions = []
    cur = con.cursor()
    cur.execute('select * from transactions')
    for result in cur:
        transaction = {}
        transaction['transaction_id'] = result[0]
        transaction['transaction_date'] = datetime.strptime(str(result[1]),'%Y-%m-%d %H:%M:%S').strftime('%d.%m.%y')
        transaction['product_id'] = result[2]
        transaction['client_id'] = result[3]
        transactions.append(transaction)
    cur.close()
    return render_template("Transactions.html", transactions= transactions)

#when we add a transaction, substract the price of the product from clients wallet
@app.route('/addTransaction', methods = ["GET", "POST"])
def addTransaction():
    if request.method == 'POST':
        values = []
        values.append("'" +  datetime.strptime(str(request.form['T_Date']),'%d.%m.%Y').strftime('%d-%b-%y') +"'")
        values.append("'" + request.form['Product_Id'] + "'")
        values.append("'" + request.form['Client_Id'] + "'")
        fields = ['transaction_date', 'videogames_product_id', 'clients_client_id']
        cur = con.cursor()
        sql = 'INSERT INTO %s (%s) VALUES (%s)' % ('transactions',', '.join(fields),', '.join(values))
        cur.execute(sql)
        cur.execute('select price from VideoGames where product_id = :ID',ID= request.form.get('Product_Id'))
        for result in cur:
            price = result[0]
        cur.execute('select wallet from Clients where client_id = :ID', ID=request.form.get('Client_Id'))
        for result in cur:
            wallet = result[0]
        if(wallet - price >= 0 ):
            cur.execute('update clients set wallet = wallet - :price where client_id = :c_id',price= price, c_id=request.form.get('Client_Id'))
        else:
            return 'Insufficient funds.Transaction could not be processed'
        cur.execute('commit')
        cur.close()
        return redirect('/Transactions')
    else:
        return render_template("addTransaction.html")

#refund clients money when deleting a transaction
@app.route('/delTransaction', methods = ["GET", "POST"])
def delTransaction():
    if request.method == 'POST':
        Transaction_ID = request.form.get('Transaction_ID')
        cur = con.cursor()
        cur.execute('select clients_client_id, videogames_product_id from transactions where transaction_id = :ID', ID=Transaction_ID)
        for result in cur:
            client_id = result[0]
            product_id = result[1]
        cur.execute('select price from VideoGames where product_id = :ID',ID=product_id)
        for result in cur:
            price = result[0]
        cur.execute('update clients set wallet = wallet + :price where client_id = :c_id',price= price, c_id=client_id)
        cur.execute('delete from transactions where transaction_id = :ID', ID=Transaction_ID)
        cur.execute('commit')
        cur.close()
        return redirect('/Transactions')
    else:
        return render_template("delTransaction.html")


if __name__ == '__main__':
    app.run(debug=True)




