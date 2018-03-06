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
        restaurantName = request.values.get('RestaurantName')
        restaurant.name = restaurantName
        session.commit()
        return redirect("", code=302)
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        session.delete(restaurant)
        session.commit()
        return redirect("", code=302)
    else:
        restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
        return render_template('deleteRestaurant.html', restaurant = restaurant)

#WORKS PERFECTLY
@app.route('/restaurant/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return render_template('menu.html', menu = menu, restaurant = restaurant, restaurant_id = restaurant_id)

#NEEDS CREATE TO WORK
@app.route('/restaurant/<int:restaurant_id>/menu/new')
def newMenuItem(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).first()
    return render_template('newMenuItem.html', restaurant = restaurant, restaurant_id = restaurant_id)

#NEEDS UPDATE TO WORK
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit')
def editMenuItem(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).first()
    return render_template('editMenuItem.html', item = item, restaurant_id = restaurant_id, menu_id = menu_id)

#NEEDS DELETE TO WORK
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
    return render_template('deleteMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
