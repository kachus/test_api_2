from flask import Flask, request
from flask_restful import Resource, Api
app = Flask(__name__)
api = Api(app)
import uuid
cars = {678: {'car_name':'Kia Rio', 'price' : 700000, 'amount' : 9, 'dealer' : 'dealer1'},

        978: {'car_name':'Ford Focus', 'price' : 800000, 'amount' : 5, 'dealer' : 'dealer2'},
        768: {'car_name':'Toyota Corola', 'price' : 750000, 'amount' : 2, 'dealer' : 'dealer3'},
        568: {'car_name':'Honda Civik', 'price' : 890000, 'amount' : 0, 'dealer' : 'dealer1'},
        858: {'car_name':'Kia Rio', 'price' : 900000, 'amount' : 3, 'dealer' : 'dealer1'}
        }

orders = {'89' : { 'user_name': 'Zhenya', 'user_secondname':'Kach', 'car_id':678}}

dealers = {'dealer1': 'dealer info1', 'dealer2':'dealer info2', 'dealer3' :'dealer3'}

class CarsList(Resource):
  def get(self):
    list_available_cars = []
    for i in cars.keys():
      if cars[i]['amount'] > 0:
        list_available_cars.append(cars[i]['car_name'])
    app.logger.info(list_available_cars)
    if len(list_available_cars) == 0:
      return 'No cars available', 400
    return list_available_cars, 200

class Car(Resource):
  def get(self, id):
    try:
      id = int(id)
      return cars[id], 200
    except KeyError:
      return 'no such car', 404



class DealersList(Resource):
  def get(self):
    return list(dealers.keys()), 200

class Dealer(Resource):
  def get(self, dealer):
    try:
      return dealers[dealer], 200
    except KeyError:
      return 'no such dealer', 404

class CheckOut(Resource):
  def post(self, id):
    user_data = request.form
    user_name = user_data.get("user_name")
    surname = user_data.get("second_name")
    id = int(id)
    if cars[id]['amount'] > 0:
      cars[id]['amount'] -= 1
      new_order_id = str(uuid.uuid1())
      orders[new_order_id] = {'user_name' : user_name,
                                  'second_name' : surname,
                                  'car_id' : id}
      #no need for an additional check

      app.logger.info("Order was created: %s",orders[new_order_id] )
      app.logger.info("Orders: %s", orders)
      return  'order was created', 201
    else:
      return 'car is not in stock', 404
      #return 'all fields must be filled in'


class OrdersList(Resource):
  def get(self):
    if len(orders) > 0:
      return orders, 200
    else:
      return 'you have no orders', 200

class Order(Resource):
  def get(self, order_id):
    try:
      return orders[order_id]
    except:
      return 'no such order', 404

  def delete(self, order_id):
    try:
      car_id = orders[order_id]['car_id']
      deleted_order = orders.pop(order_id)
      cars[car_id]['amount'] += 1

      app.logger.info("order %s was deleted", deleted_order)
      return 'order was deleted', 200
    except:
      return 'no such order in order', 400


#cars[car_id]['amount'] += 1



api.add_resource(CarsList, '/cars')
api.add_resource(Car, '/cars/<id>')
api.add_resource(DealersList, '/dealers')
api.add_resource(Dealer, '/dealers/<dealer>')
api.add_resource(CheckOut, '/cars/<id>/checkout')
api.add_resource(OrdersList, '/orders')
api.add_resource(Order,'/orders/<order_id>')

if __name__ == "__main__":
        app.run(debug=True)







#basket = {678: {'car_name':'Kia Rio', 'price':'700000', 'dealer': 'dealer1','amount':1}}








