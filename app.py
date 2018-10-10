from flask import Flask,jsonify,__version__,g;
import sqlite3,csv;

app = Flask(__name__)

DATABASE = 'C:/Users/Sahbani/PycharmProjects/Partie1/datas.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/version',methods=['GET'])
def version():
    return jsonify({"version":__version__})

@app.route('/datas',methods=['GET'])
def datas():
    con=sqlite3.connect("datas.sqlite")
    cur=con.cursor()
    cur.execute("select * from datas  limit 20")
    rows=cur.fetchall();
    return jsonify({'datas': rows})

@app.route('/reload',methods=['POST'])
def reload():
    con = sqlite3.connect("datas.sqlite")
    cur = con.cursor()
    with open('data_file.csv', 'rt') as fin:
        types = (line.split("|") for line in fin)
        xys = ((type[0], type[1], type[2], type[3]) for type in types)
        indice=0
        for x, y,z,w in xys:
            cur.execute("replace INTO datas (id,custom_id_row, row_hash,value_1,value_2) VALUES (?,?,?, ?,?);", (indice,x,y,z,w))
            con.commit()
            indice+=1
    return "reload data successfully"

if __name__ == '__main__':
    app.run()
