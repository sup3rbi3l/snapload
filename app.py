from flask import Flask, render_template, request, redirect, url_for,send_file,after_this_request
import os
import pymysql

app = Flask(__name__)
def databaseConect():
    sql = pymysql.connect(
        host='trolley.proxy.rlwy.net',
        port=55826,
        user='root',
        password='NFKhjuHSSxPPbBKVbpwxBKTRmEQWfHxr',
        database ='railway'
    )
    return sql

sql = pymysql.connect(
        host='trolley.proxy.rlwy.net',
        port=55826,
        user='root',
        password='NFKhjuHSSxPPbBKVbpwxBKTRmEQWfHxr',
)

data = sql.cursor()

data.execute('SELECT COUNT(*) FROM information_schema.SCHEMATA WHERE SCHEMA_NAME = "railway";')
result = data.fetchone()[0]

if result > 0:
    sql.close()
    sql = databaseConect()
    print('Banco encontrado')
    
    data = sql.cursor()
    
    data.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'railway' AND table_name = 'produtos'")

    result = data.fetchone()[0]
    if result == 0:
        
        data.execute("CREATE TABLE produtos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), preco DECIMAL(10, 2),quantidade INT);")
        
        sql.commit()
        print('tabela produtos criada')
    
    else:

        print('tabela produtos ja existia')
    sql.close()

else:
    print('chegou foda')
    data.execute('CREATE DATABASE railway;')
    sql.commit()
    sql = databaseConect()
    data = sql.cursor()
    data.execute("CREATE TABLE produtos (id INT AUTO_INCREMENT PRIMARY KEY, nome VARCHAR(255), preco DECIMAL(10, 2),quantidade INT);")
    sql.commit()
    sql.close()

@app.route('/produtos')
def produtos():
    sql = databaseConect()
    data = sql.cursor()
    data.execute('SELECT * FROM produtos')
    table_data = data.fetchall()
   
    
    return render_template('produtos.html',table_data=table_data)


@app.route('/delete_product/<id>',methods=['GET', 'POST'])
def delete_product(id):
    print(id)
    sql = databaseConect()
    data = sql.cursor()
    data.execute("""
        DELETE FROM produtos
        WHERE id = %s;
    """,(id,))
    
    sql.commit()
    sql.close
    
    return redirect(url_for('produtos'))
    
@app.route('/add_products',methods=["POST","GET"])
def add_products():
    
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    
    print(name,price,quantity)
    if name == None or name == '':
        return render_template('add_produtos.html',error='erro') 
    
    
    
    sql = databaseConect()
    data = sql.cursor()
    data.execute('INSERT INTO produtos(nome,preco,quantidade) VALUES (%s,%s,%s)',(name,price,quantity))
    
    sql.commit()
    sql.close()
    
    return render_template('add_produtos.html')

@app.route('/update_product/<id>',methods=['GET', 'POST'])
def update_product(id):
    name = request.form.get('name')
    price = request.form.get('price')
    quantity = request.form.get('quantity')
    
    
    
    print(name,price,quantity)
    if request.method == 'POST':
        
        if name == None or name == '':
            return render_template('add_produtos.html',error='erro') 
    
        sql = databaseConect()
        data = sql.cursor()
        data.execute('UPDATE produtos SET nome = %s,  preco = %s, quantidade = %s WHERE id = %s;',(name,price,quantity,id))
        
        sql.commit()
        sql.close()
        
        return redirect(url_for('produtos'))
        
    return render_template('update_product.html',id = id)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # usa a porta definida pelo Railway
    app.run(host='0.0.0.0', port=port, debug=True)