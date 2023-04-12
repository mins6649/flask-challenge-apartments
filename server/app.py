from flask import Flask, make_response, request #add request
from flask_migrate import Migrate
from flask_restful import Api, Resource

# add (Apartment, Tenant, Lease)
from models import db, Apartment, Tenant, Lease

app = Flask( __name__ )
app.config[ 'SQLALCHEMY_DATABASE_URI' ] = 'sqlite:///apartments.db'
app.config[ 'SQLALCHEMY_TRACK_MODIFICATIONS' ] = False

migrate = Migrate( app, db )
db.init_app( app )
# added API
api = Api(app)

class Apartment(Resource):
    def get(self):
        
        apartment_dict_list = [a.to_dict() for a in Apartment.query.all()]

        response = make_response(
            apartment_dict_list,
            200
        ) 
        return response
    
    def post(self):
        
        new_apartment = Apartment(
            number = request.form['number'],
        )

        db.session.add(new_apartment)
        db.session.commit()

        response_dict = new_apartment.to_dict()

        response = make_response(
            response_dict,
            201,
        )

        return response


api.add_resource(Apartment, '/apartment')

class ApartmentById(Resource):
    def get(self, id):
        
        response_dict = Apartment.query.filter_by(id=id).first().to_dict()

        response = make_response(
            response_dict,
            200
        )
        return response
    
    def patch(self, id):
        
        record = Apartment.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(record, attr, request.form[attr])

        db.session.add(record)
        db.session.commit()

        response_dict = record.to_dict()

        response = make_response(
            response_dict,
            200
        )
        return response

    def delete(self, id):
        
        record = Apartment.query.filter_by(id=id).first()

        db.session.delete(record)
        db.session.commit()

        response_dict = {"message": "record successfully deleted"}

        response = make_response(
            response_dict,
            200
        )

        return response

api.add_resource(Apartment, '/apartment/<int:id>')

if __name__ == '__main__':
    app.run( port = 3000, debug = True )