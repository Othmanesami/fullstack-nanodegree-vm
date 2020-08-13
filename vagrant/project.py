from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind= engine)



#@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):

    session = DBSession()
    
    restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id= restaurant_id)

    return render_template('menu.html', restaurant= restaurant, items= items)



@app.route('/restaurants/<int:restaurant_id>/new/', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':

        session = DBSession()

        newItem = MenuItem(name= request.form['name'], restaurant_id= restaurant_id)
        session.add(newItem)
        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:
        
        return render_template('newmenuitem.html', restaurant_id= restaurant_id)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':

        session = DBSession()

        editItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
        editItem.name = request.form['name']
        session.add(editItem)
        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))

    else:

        session = DBSession()
        
        item = session.query(MenuItem).filter_by(restaurant_id= restaurant_id, id=menu_id).one()
        item_name = item.name

        return render_template('editmenuitem.html', restaurant_id= restaurant_id, menu_id= menu_id, item_name=item_name)



@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    if request.method == 'POST':

        session = DBSession()

        deleteItem = session.query(MenuItem).filter_by(restaurant_id = restaurant_id, id=menu_id).one()
        session.delete(deleteItem)
        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id= restaurant_id))

    else:

        session = DBSession()

        item = session.query(MenuItem).filter_by(restaurant_id= restaurant_id, id=menu_id).one()
        item_name = item.name
        return render_template('deletemenuItem.html', restaurant_id= restaurant_id, menu_id= menu_id, item_name=item_name)
    




if __name__ == "__main__":

    app.debug = True
    app.run(host= '0.0.0.0', port= 5000)