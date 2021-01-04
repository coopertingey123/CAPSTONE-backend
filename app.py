from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_heroku import Heroku
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://gzrkczxqihabxm:89fcdcec42ee20182d9ba09e49d32bb6f4361f8e02e9bf92c23a6b5bb811531d@ec2-54-208-233-243.compute-1.amazonaws.com:5432/d4p6ks1t0hops9"

db = SQLAlchemy(app)
ma = Marshmallow(app)
bcrypt = Bcrypt(app)

CORS(app)
Heroku(app)

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(40), unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    phone_number = db.Column(db.String(20), unique=False, nullable=False)


    def __init__(self, email, password, first_name, last_name, phone_number):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number

class OwnerSchema(ma.Schema):
    class Meta:
        fields = ("id", "email", "password", "first_name", "last_name", "phone_number")

owner_schema = OwnerSchema()
multiple_Owner_schema = OwnerSchema(many=True)


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), unique=False, nullable=False)
    last_name = db.Column(db.String(20), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    address= db.Column(db.String(50), unique=False, nullable=False)
    phone_number= db.Column(db.String(20), unique=True, nullable=False)
    day_of_week= db.Column(db.String(20), unique=False, nullable=False)
    info_for_owner= db.Column(db.String(300), unique=False, nullable=True)
    owner_email= db.Column(db.String(40), unique=False, nullable=False)

    def __init__(self, first_name, last_name, email, address, phone_number, day_of_week, info_for_owner, owner_email):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.phone_number = phone_number
        self.day_of_week = day_of_week
        self.info_for_owner = info_for_owner
        self.owner_email = owner_email

class ClientSchema(ma.Schema):
    class Meta:
        fields = ("id", "first_name", "last_name", "email", "address", "phone_number", "day_of_week", "info_for_owner", "owner_email")

client_schema = ClientSchema()
multiple_clients_schema = ClientSchema(many=True)


@app.route("/business-owner/add", methods=["POST"])
def create_business_owner():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    phone_number = post_data.get("phone_number")

    existingOwner = db.session.query(Owner).filter(Owner.email == email).first()
    if existingOwner is not None:
        return jsonify("Owner already exists")

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    record = Owner(email, password_hash, first_name, last_name, phone_number)
    db.session.add(record)
    db.session.commit()

    return jsonify("Owner added successfully")

@app.route("/client/add", methods=["POST"])
def create_client():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    first_name = post_data.get("first_name")
    last_name = post_data.get("last_name")
    email = post_data.get("email")
    address = post_data.get("address")
    phone_number = post_data.get("phone_number")
    day_of_week = post_data.get("day_of_week")
    info_for_owner = post_data.get("info_for_owner")
    owner_email = post_data.get("owner_email")

    existingClient = db.session.query(Client).filter(Client.email == email).first()
    if existingClient is not None:
        return jsonify("Client already exists")

    record = Client(first_name, last_name, email, address, phone_number, day_of_week, info_for_owner, owner_email)
    db.session.add(record)
    db.session.commit()
    
    return jsonify("Client added successfully")

@app.route("/client/get", methods=["GET"])
def get_all_clients():
    all_clients = db.session.query(Client.id, Client.first_name, Client.last_name, Client.email, Client.address, Client.phone_number, Client.day_of_week, Client.info_for_owner, Client.owner_email).all()
    return jsonify(multiple_clients_schema.dump(all_clients))

@app.route("/client/delete/<email>", methods=["DELETE"])
def delete_client(email):
    one_client = db.session.query(Client).filter(Client.email == email).first()
    db.session.delete(one_client)
    db.session.commit()
    return jsonify(f"Client with email {email} was deleted")


@app.route("/book/delete/<title>", methods=["DELETE"])
def delete_book_by_title(title):
    record = db.session.query(Book).filter(Book.title == title).first()
    db.session.delete(record)
    db.session.commit()
    return jsonify(f"Book with title {title} was successfully deleted")



@app.route("/client/names/get", methods=["GET"])
def get_all_client_names():
    all_client_names = db.session.query(Client.first_name, Client.last_name).all()

    return jsonify(multiple_clients_schema.dump(all_client_names))

@app.route("/client/get/marshmallow", methods=["GET"])
def get_all_clients_marshmallow():
    # all_clients = Client.query.all()
    all_clients = db.session.query(Client).all()
    return jsonify(multiple_clients_schema.dump(all_clients))






@app.route("/client/get/my-clients/<owner_email>", methods=["GET"])
def get_my_clients(owner_email):

    my_clients = db.session.query(Client).filter(Client.owner_email == owner_email).all()

    return jsonify(multiple_clients_schema.dump(my_clients))




@app.route("/owners/get", methods=["GET"])
def get_all_owners():
    all_owners = db.session.query(Owner).all()
    return jsonify(multiple_Owner_schema.dump(all_owners))


@app.route("/owner/authentication", methods=["POST"])
def owner_authentication():
    if request.content_type != "application/json":
        return "Error: Data must be sent as JSON."

    post_data = request.get_json()
    email = post_data.get("email")
    password = post_data.get("password")

    owner = db.session.query(Owner).filter(Owner.email == email).first()

    if email is None:
        return jsonify("Invalid Credentials")

    if bcrypt.check_password_hash(owner.password, password) != True:
        return jsonify("Invalid Credentials")

    return {
        "status": "logged_in"
    }


if __name__ == "__main__":
    app.run(debug=True)