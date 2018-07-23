from flask import Flask, jsonify
from mongoengine import *
from flask_restful import Resource, Api, reqparse
from datetime import datetime
from models import *

# Initialize the app and connect to the db
# TODO: Setup environment specific configs
app = Flask(__name__)
api = Api(app)
connect('test', host='db')

class TicketSimple(Resource):
    def get(self, ticket_id):
        try:
            return Ticket.objects.get(id=ticket_id).to_json()
        except:
            return {'error': 'Object with id: ' + ticket_id + ' not found'}, 500

    def put(self, ticket_id):
        try:
            root_parser = reqparse.RequestParser()
            root_parser.add_argument('assigned_to', type=dict)
            root_parser.add_argument('status', type=str)
            root_parser.add_argument('comment', type=str)
            args = root_parser.parse_args()
            
            ticket = Ticket.objects.get(id=ticket_id)

            #TODO: Request paramater validation
            
            # Assign a ticket to someone
            if('assigned_to' in args):
                name = args['assigned_to']['name']
                email = args['assigned_to']['email']
                ticket.assigned_to = User(name, email)

            # Change the status of a ticket
            if('status' in args):
                new_status = args['status']
                # TODO: Validate that the status is a valid one.
                Ticket.status = new_status

            # Add a comment
            if('comment' in args):
                comment = Comment(content = args['comment'])
                ticket.add_or_replace_comment(comment)


            ticket.save()
        except Exception as e:
            return str(e), 500


class TicketList(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('status', type=str, store_missing=False)
            parser.add_argument('date', type=int, store_missing=False)
            args = parser.parse_args()

            query = None

            # TODO: Validate params

            # Get tickets with a specific status
            if('status' in args):
                query = Q(status=args['status'])

            # Get tickets that were created after the given date
            if('date' in args):
                query_date = datetime.fromtimestamp(args['date']/1000.0)
                if(query):
                    query = query | Q(created_at__lte = query_date)
                else:
                    query = Q(created_at__lte = query_date)

            
            print(query)
            return Ticket.objects(query).to_json()
        except Exception as e:
            return str(e), 500
        


api.add_resource(TicketList, '/tickets')
api.add_resource(TicketSimple, '/tickets/<ticket_id>')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

    
