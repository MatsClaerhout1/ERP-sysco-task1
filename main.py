import os
import requests
from flask import Flask
from flask_restful import Api, Resource, reqparse, fields, marshal_with, abort
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# -------------------- Models --------------------
@app.route('/')
def home():
    return "Welcome to the API mathafacker!"

# Comic Strip model
class StripModel(db.Model):
    strip_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    publicationYear = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Strip(strip_id={self.strip_id}, title={self.title}, author={self.author}, year={self.publicationYear}, genre={self.genre})"

# User model
class UserModel(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100), nullable=False)
    lastName = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"User(user_id={self.user_id}, name={self.firstName} {self.lastName}, email={self.email}, city={self.city})"

# Collection model (relating users and strips)
class CollectionModel(db.Model):
    collection_id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user_model.user_id'), nullable=False)
    stripId = db.Column(db.Integer, db.ForeignKey('strip_model.strip_id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"Collection(collection_id={self.collection_id}, userId={self.userId}, stripId={self.stripId}, status={self.status})"

# -------------------- Parsers --------------------

# Strip parser
strip_put_args = reqparse.RequestParser()
strip_put_args.add_argument("title", type=str, help="Title of the strip is required", required=True)
strip_put_args.add_argument("author", type=str, help="Author of the strip is required", required=True)
strip_put_args.add_argument("publicationYear", type=int, help="Publication year is required", required=True)
strip_put_args.add_argument("genre", type=str, help="Genre is required", required=True)

strip_update_args = reqparse.RequestParser()
strip_update_args.add_argument("title", type=str)
strip_update_args.add_argument("author", type=str)
strip_update_args.add_argument("publicationYear", type=int)
strip_update_args.add_argument("genre", type=str)

# User parser
user_put_args = reqparse.RequestParser()
user_put_args.add_argument("firstName", type=str, help="First name is required", required=True)
user_put_args.add_argument("lastName", type=str, help="Last name is required", required=True)
user_put_args.add_argument("city", type=str, help="City is required", required=True)
user_put_args.add_argument("email", type=str, help="Email is required", required=True)

user_update_args = reqparse.RequestParser()
user_update_args.add_argument("firstName", type=str)
user_update_args.add_argument("lastName", type=str)
user_update_args.add_argument("city", type=str)
user_update_args.add_argument("email", type=str)

# Collection parser
collection_put_args = reqparse.RequestParser()
collection_put_args.add_argument("userId", type=int, help="User ID is required", required=True)
collection_put_args.add_argument("stripId", type=int, help="Strip ID is required", required=True)
collection_put_args.add_argument("status", type=str, help="Status is required", required=True)

collection_update_args = reqparse.RequestParser()
collection_update_args.add_argument("status", type=str)

# -------------------- Resource Fields --------------------

strip_fields = {
    'strip_id': fields.Integer,
    'title': fields.String,
    'author': fields.String,
    'publicationYear': fields.Integer,
    'genre': fields.String
}

user_fields = {
    'user_id': fields.Integer,
    'firstName': fields.String,
    'lastName': fields.String,
    'city': fields.String,
    'email': fields.String
}

collection_fields = {
    'collection_id': fields.Integer,
    'userId': fields.Integer,
    'stripId': fields.Integer,
    'status': fields.String
}

# -------------------- Resources --------------------

# Strip resource
class Strip(Resource):
    @marshal_with(strip_fields)
    def get(self, strip_id):
        result = StripModel.query.filter_by(strip_id=strip_id).first()
        if not result:
            abort(404, message="Could not find strip with that id")
        return result

    @marshal_with(strip_fields)
    def getAll(self):
        result = StripModel.query.all()  # Fetch all strips from the database
        if not result:
            abort(404, message="No strips found")  # Optional: Handle no strips case
        return result

    @marshal_with(strip_fields)
    def put(self, strip_id):
        args = strip_put_args.parse_args()
        result = StripModel.query.filter_by(strip_id=strip_id).first()
        if result:
            abort(409, message="Strip id taken...")
        strip = StripModel(strip_id=strip_id, title=args['title'], author=args['author'], publicationYear=args['publicationYear'], genre=args['genre'])
        db.session.add(strip)
        db.session.commit()
        return strip, 201

    @marshal_with(strip_fields)
    def patch(self, strip_id):
        args = strip_update_args.parse_args()
        result = StripModel.query.filter_by(strip_id=strip_id).first()
        if not result:
            abort(404, message="Strip doesn't exist, cannot update")
        if args['title']:
            result.title = args['title']
        if args['author']:
            result.author = args['author']
        if args['publicationYear']:
            result.publicationYear = args['publicationYear']
        if args['genre']:
            result.genre = args['genre']
        db.session.commit()
        return result

    def delete(self, strip_id):
        result = StripModel.query.filter_by(strip_id=strip_id).first()
        if not result:
            abort(404, message="Could not find strip with that id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

# User resource
class User(Resource):
    @marshal_with(user_fields)
    def get(self, user_id):
        result = UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        return result

    @marshal_with(user_fields)
    def put(self, user_id):
        args = user_put_args.parse_args()
        result = UserModel.query.filter_by(user_id=user_id).first()
        if result:
            abort(409, message="User id taken...")
        user = UserModel(user_id=user_id, firstName=args['firstName'], lastName=args['lastName'], city=args['city'], email=args['email'])
        db.session.add(user)
        db.session.commit()
        return user, 201

    @marshal_with(user_fields)
    def patch(self, user_id):
        args = user_update_args.parse_args()
        result = UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="User doesn't exist, cannot update")
        if args['firstName']:
            result.firstName = args['firstName']
        if args['lastName']:
            result.lastName = args['lastName']
        if args['city']:
            result.city = args['city']
        if args['email']:
            result.email = args['email']
        db.session.commit()
        return result

    def delete(self, user_id):
        result = UserModel.query.filter_by(user_id=user_id).first()
        if not result:
            abort(404, message="Could not find user with that id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

# Collection resource
class Collection(Resource):
    @marshal_with(collection_fields)
    def get(self, collection_id):
        result = CollectionModel.query.filter_by(collection_id=collection_id).first()
        if not result:
            abort(404, message="Could not find collection with that id")
        return result

    @marshal_with(collection_fields)
    def put(self, collection_id):
        args = collection_put_args.parse_args()
        result = CollectionModel.query.filter_by(collection_id=collection_id).first()
        if result:
            abort(409, message="Collection id taken...")
        collection = CollectionModel(collection_id=collection_id, userId=args['userId'], stripId=args['stripId'], status=args['status'])
        db.session.add(collection)
        db.session.commit()
        return collection, 201

    @marshal_with(collection_fields)
    def patch(self, collection_id):
        args = collection_update_args.parse_args()
        result = CollectionModel.query.filter_by(collection_id=collection_id).first()
        if not result:
            abort(404, message="Collection doesn't exist, cannot update")
        if args['status']:
            result.status = args['status']
        db.session.commit()
        return result

    def delete(self, collection_id):
        result = CollectionModel.query.filter_by(collection_id=collection_id).first()
        if not result:
            abort(404, message="Could not find collection with that id")
        db.session.delete(result)
        db.session.commit()
        return '', 204

# -------------------- API Routes --------------------

api.add_resource(Strip, '/strips/<int:strip_id>')
api.add_resource(User, '/users/<int:user_id>')
api.add_resource(Collection, '/collections/<int:collection_id>')

# -------------------- Main --------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Read the port from environment variables
    app.run(host="0.0.0.0", port=port)
