from flask import Flask, render_template, request, redirect, url_for
from database_setup import db, Product, init_db

app = Flask(__name__)
init_db(app)

@app.route('/')
def shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = float(request.form['price'])
        image_url = request.form['image_url']
        new_product = Product(name=name, description=description, price=price, image_url=image_url)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('shop'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'POST':
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.image_url = request.form['image_url']
        db.session.commit()
        return redirect(url_for('shop'))
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>')
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('shop'))

# Additional Pages
@app.route('/shops')
def shops():
    return render_template('shops.html')

@app.route('/products')
def products():
    return render_template('products.html')

@app.route('/bids')
def bids():
    return render_template('bids.html')

@app.route('/your-shop')
def your_shop():
    products = Product.query.all()
    return render_template('shop.html', products=products)

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

if __name__ == '__main__':
    app.run(debug=True)
