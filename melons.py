from flask import Flask, request, session, render_template, g, redirect, url_for, flash
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """TODO: Display the contents of the shopping cart. The shopping cart is a
    list held in the session that contains all the melons to be added. Check
    accompanying screenshots for details."""
    
    if 'cart' in session:
        if 'cart' != {}:
            cart_items = session['cart']   

            melon_details = []

            for id, quantity in cart_items.iteritems():
                melon = model.get_melon_by_id(id)
                melon_dict = {
                    "name": melon.common_name,
                    "price": melon.price,
                    "quantity": quantity,
                    "total": melon.price * quantity
                }
                melon_details.append(melon_dict)

            order_total = 0
            for melon in melon_details:
                order_total += melon['total']

            return render_template("cart.html", melons = melon_details, 
                                                order_total = order_total)
    else:
        return render_template("cart.html", melons = None, order_total = 0)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """TODO: Finish shopping cart functionality using session variables to hold
    cart list.

    Intended behavior: when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """

    id = str(id)

    if 'cart' in session:
        if id in session['cart']:
            session['cart'][id] += 1
        else:
            session['cart'][id] = 1
    else:
        session['cart'] = {id:1}

    flash("Item added to cart.")
    return redirect("/cart")

@app.route("/sessionclear", methods=["GET"])
def sessionclear():
    session.clear()
    return "BOOM!"

@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")

# need a logout function - remove customer from session (?) and redirect to "logout " page

@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    customer = model.get_customer_by_email(email,password)
    print customer

    if customer == None:
        flash("No user found for that email/password combination.")
        return redirect("/login")
    else:   # Is there need for a logged_in = True?
        session["current_user"] = { "logged_in": True,
                                    "customer_id": customer.id,
                                    "first_name": customer.first,
                                    "last_name": customer.last}
        flash("Welcome, " + session["current_user"]["first_name"] + ".")
        return redirect("/melons")

@app.route("/logout")
def process_logout():
    del session["current_user"]
    # session["current_user"] = {}
    flash("Logged out.")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

@app.route('/clearcart')
def clear_cart():
    session['cart'] = {}
    return redirect("/cart")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
