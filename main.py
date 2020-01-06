from flask import Flask, render_template, make_response, request, redirect, url_for
from models import User, db
from random import randint, seed
import uuid
import hashlib

seed(100)

db.create_all()

app = Flask(__name__)

@app.route("/")
def index():
  token = request.cookies.get("token")
  user = db.query(User).filter_by(token=token).first()
  if user is None:
    response = make_response(
      redirect(url_for("login_get"))
    )
    return response
  else:
    print (user.email, user.name)  
    #return "<h1>Glavna stran</h1>"
    return render_template("guess.html")

@app.route("/", methods=["POST"])
def index_post():
  token = request.cookies.get("token")
  user = db.query(User).filter_by(token=token).first()
  guessed = False
  
  if user is None:
    response = make_response(
      redirect(url_for("login_get"))
    )
    return response
  vpisana_st = int(request.form.get("ugibanje"))
  if vpisana_st > user.secret_number:
    message = "Vpisana številka je prevelika"
  elif vpisana_st < user.secret_number:
    message = "Vpisana številka je premajhna"
  else:
    message = "Vpisana številka je pravilna"
    guessed = True
    
  return render_template("result_guess.html", message=message, guessed=guessed)

@app.route("/reset")
def reset():
  token = request.cookies.get("token")
  user = db.query(User).filter_by(token=token).first()
  
  if user is None:
    response = make_response(
      redirect(url_for("login_get"))
    )
    return response
  
  user.secret_number = randint(0,100)
  print(user.secret_number)
  
  db.add(user)
  db.commit()
  response = make_response(
      redirect(url_for("index"))
    )
  return response


@app.route("/login", methods=["GET"])
def login_get():
  return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
  name = request.form.get("name")
  email = request.form.get("email")
  password = hashlib.sha512(request.form.get("password").encode()).hexdigest()
  print(password)
  number = randint(0, 10)
  print(number)
  user = db.query(User).filter_by(email=email).first()
  
  if user is not None:
    if user.password != password:
      return "<h1> Wrong Username or Password! </h1>"
  
  else:
    user = User(name=name, email=email, secret_number=number, password=password, token=str(uuid.uuid4()))
    db.add(user)
    db.commit()   
  
  response = make_response(
    redirect(url_for("index"))
    )
  response.set_cookie("token", user.token)
  
  return response

if __name__ == "__main__":
    app.run()