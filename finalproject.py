from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

#WORKS
@app.route('/')
@app.route('/restaurants')
def showRestaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants = restaurants)
#WORKS
@app.route('/restaurant/new', methods=['GET', 'POST'])
def newRestaurant():
    if request.method == 'POST':
        restaurantName = Restaurant(name = request.values.get('RestaurantName'))
        session.add(restaurantName)
        session.commit()
        return redirect("", code=302)
    else:
        return render_template('newRestaurant.html')

#WORKS
@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    if request.method == 'POST':
        restaurant.name = request.values.get('RestaurantName')
        session.commit()
        return redirect("", code=302)
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        session.delete(restaurant)
        session.commit()
        return redirect("", code=302)

#WORKS
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', menu = menu, restaurant = restaurant, restaurant_id = restaurant_id)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    if request.method == 'POST':
        Item = MenuItem(name = request.values.get('ItemName'), description = request.values.get('Description'), price = request.values.get('Price'), course = request.values.get('Course'), restaurant = restaurant)
        session.add(Item)
        session.commit()
        return redirect("", code=302)
    else:
        return render_template('newMenuItem.html', restaurant = restaurant, restaurant_id = restaurant_id)
    
#WORKS
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    if request.method == 'POST':
        item.name = request.values.get('ItemName')
        item.description = request.values.get('Description')
        item.price = request.values.get('Price')
        item.course = request.values.get('Course')
        session.commit()
        return redirect("", code=302)
    else:
        return render_template('editMenuItem.html', item = item, restaurant_id = restaurant_id, menu_id = menu_id)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
        item = session.query(MenuItem).filter_by(id = menu_id).first()
        session.delete(item)
        session.commit()
        return redirect("", code=302)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
