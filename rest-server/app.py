from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

count = 0


class Counter(Resource):
    def get(self):
        global count
        count = count+1
        return count, 200

    def post(self):
        global count
        count = count+1
        return count, 200


api.add_resource(Counter, "/counter")

app.run(host='0.0.0.0', debug=True)
