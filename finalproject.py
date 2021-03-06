from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


app = Flask(__name__)
app.secret_key = 'some_secret'

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
        flash('New Restaurant Created')
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
        flash('Restaurant Successfully Edited')
        return redirect("", code=302)
    else:
        return render_template('editRestaurant.html', restaurant = restaurant)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/delete')
def deleteRestaurant(restaurant_id):
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
        session.delete(restaurant)
        session.commit()
        flash('Restaurant Successfully Deleted')
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
        flash('New Menu Item Created')
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
        flash('Menu Item Successfully Edited')
        return redirect("", code=302)
    else:
        return render_template('editMenuItem.html', item = item, restaurant_id = restaurant_id, menu_id = menu_id)

#WORKS
@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete')
def deleteMenuItem(restaurant_id, menu_id):
        item = session.query(MenuItem).filter_by(id = menu_id).first()
        session.delete(item)
        session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect("", code=302)

@app.route('/restaurant/JSON')
def restaurantsJSON():
    restaurant = session.query(Restaurant).all()
    return jsonify(Restaurants = [i.serialize for i in restaurant])

@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurantsMenuJSON(restaurant_id):
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    return jsonify(MenuItems = [i.serialize for i in menu])

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantsMenuItemJSON(restaurant_id, menu_id):
    menu = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
    for i in menu:
        if i.restaurant_id == restaurant_id and i.id == menu_id:
            return jsonify(i.serialize)
    return "No Item"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
