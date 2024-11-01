import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__));

database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"));

app = Flask(__name__);

app.config["SQLALCHEMY_DATABASE_URI"] = database_file;

db = SQLAlchemy(app);

class Book(db.Model):
    title = db.Column(db.String(80), unique = True, nullable = False, primary_key = True);
    autor = db.Column(db.String(80), nullable = True);
    genero = db.Column(db.String(80), nullable = True);
    num_pag = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return "<Title: {}>".format(self.title);
    
    def __repr__(self):
        return "<Autor: {}>".format(self.autor);

    def __repr__(self):
        return "<Genero: {}>".format(self.genero);

    def __repr__(self):
        return "<Num_pag: {}>".format(self.num_pag);


@app.route('/', methods=["GET","POST"])
def home():
    books = None 
    if request.form:
        try:
            book = Book(title = request.form.get("title"))
            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print("Falha ao adicionar livro")
            print(e)

    books = Book.query.all()
    return render_template("index.html", books=books)


@app.route("/update",methods=["POST"])
def update():
    try:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        newtitle = request.form.get("newtitle")
        oldtitle = request.form.get("oldtitle")

        newautor = request.form.get("newautor")
        oldautor = request.form.get("oldautor")

        newgenero = request.form.get("newgenero")
        oldgenero = request.form.get("oldgenero")

        newnum_pag = request.form.get("newnum_pag")
        oldnum_pag = request.form.get("oldnum_pag")

        book = Book.query.filter_by(title=oldtitle).first()
        book.title = newtitle

        book = Book.query.filter_by(title=oldautor).first()
        book.autor = newautor

        book = Book.query.filter_by(title=oldgenero).first()
        book.genero = newgenero

        book = Book.query.filter_by(title=oldnum_pag).first()
        book.num_pag = newnum_pag
        
        db.session.commit()


    except Exception as e:
        print("Não dá pra fazer update")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)