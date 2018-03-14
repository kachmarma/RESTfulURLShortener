from flask import Flask, redirect
from flask_restful import reqparse, abort, Api, Resource
import baseConversion
import json
import sqlite3

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('URL')

# URL
class URL(Resource):
    def get(self, url_id):
        converted_id = (str(baseConversion.to10(url_id)),)
        print("ID converted to base10 for db lookup: %s", converted_id)
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('SELECT url FROM urls WHERE ID = ?', converted_id)
        url = c.fetchone()[0]
        c.close()
        return redirect(url, code=302)
    
    def delete(self, url_id):
        convertred_id = str(baseConversion.to10(url_id))
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('DELETE FROM urls WHERE ID = ?', convertred_id)
        conn.commit()
        c.close()
        return '', 204

    def put(self, url_id):
        args = parser.parse_args()
        print(args)
        task = str(args['URL'])
        converted_id = int(baseConversion.to10(url_id))
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        print(task)
        print(converted_id)
        c.execute('UPDATE urls SET url = ? WHERE ID = ?;', [task, converted_id])
        conn.commit()
        return task, 201

# URLs
class URLList(Resource):
    def get(self):
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('SELECT * FROM urls')
        return c.fetchall()

    def post(self):
        # havent done this yetasd
        args = parser.parse_args()
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        symbol = (str(args['URL']),)
        c.execute('INSERT INTO urls (url) VALUES(?)', symbol)
        c.execute('SELECT seq FROM sqlite_sequence')
        url_id = c.fetchone()[0]
        conn.commit()
        c.close()
        print(baseConversion.to62(int(url_id)))
        return "http://localhost:5000/urls/{}".format(baseConversion.to62(int(url_id))), 201

    def delete(self):
        conn = sqlite3.connect('urls.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS urls')
        c.execute('CREATE TABLE urls (ID INTEGER PRIMARY KEY AUTOINCREMENT, url TEXT NOT NULL);')
        conn.commit()
        return '', 200

# Actually set up the API resource routing here
api.add_resource(URLList, '/urls', '/')
api.add_resource(URL, '/urls/<url_id>')

if __name__ == '__main__':
    app.run(debug=True)