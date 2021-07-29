from threading import Timer
import webbrowser
from flask import (Flask,
                   request,
                   render_template,
                   redirect,
                   url_for,
                   send_file)
from constants import (resource_path,
                       make_directory_for_user_db,
                       SEARCH_HEADER,
                       CACHES,
                       CACHE_NAMES,
                       NFES_RNG,
                       CLASS,
                       CATEGORIES,
                       CART_HEADER,
                       ORDERS_HEADER,
                       LISTS_HEADER)
from worker import Worker

app = Flask(__name__, template_folder=resource_path('templates'), static_folder=resource_path('static'))


@app.route('/', methods=['POST', 'GET'])
def home():
    return render_template('home.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    flash = None
    user_db = app.config['USER_DB_PATH']
    if request.method == 'POST':
        user = request.form['user']
        if Worker.check_user(user_db, user):
            app.config['FIREUSER'] = Worker.get_user(user_db, user)
            w = app.config['FIREUSER']
            return redirect(url_for('search', cache=w.cache, sort=w.sort, prev_sort=w.prev_sort, reverse=0))
        else:
            flash = 'Username not in database'
    return render_template('login.html', flash=flash)


@app.route('/create', methods=['POST', 'GET'])
def create():
    flash = None
    user_db = app.config['USER_DB_PATH']
    if request.method == 'POST':
        new = request.form['new']
        if new == '':
            flash = 'Please enter a username'
        else:
            if Worker.check_user(user_db, new):
                flash = f'User "{new}" already in database, please enter a new username or Login'
            else:
                w = Worker(new)
                w.insert_self(user_db)
                app.config['FIREUSER'] = w
                return redirect(url_for('search', cache=w.cache, sort=w.sort, prev_sort=w.prev_sort, reverse=w.reverse))
    return render_template('create.html', flash=flash)


@app.route('/exit')
def exit():
    try:
        w = app.config['FIREUSER']
        w.update_self(app.config['USER_DB_PATH'])
    except KeyError:
        pass
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    return 'Server is shutting down...<br /><br />You can exit the browser'


@app.route('/delete_user', methods=['POST', 'GET'])
def delete_user():
    flash = None
    if request.method == 'POST':
        if Worker.check_user(app.config['USER_DB_PATH'], request.form['user']):
            Worker.delete_user(app.config['USER_DB_PATH'], request.form['user'])
            flash = f"""User {request.form['user']} deleted successfully"""
        else:
            flash = f"""User {request.form['user']} not in database"""
    return render_template('delete_user.html', flash=flash)


@app.route('/<cache>_<sort>_<prev_sort>_<reverse>', methods=['POST', 'GET'])
def search(cache, sort, prev_sort, reverse):
    w = app.config['FIREUSER']
    w.cache = cache
    w.sort = sort
    w.prev_sort = prev_sort
    w.reverse = reverse
    flash = None
    if request.method == 'POST':
        for key in request.form:
            if key[:3] != 'cbx':
                if key not in ['select_all', 'list', 'list_on']:
                    if key == 'nfes' and request.form[key] != 'all':
                        w[key] = [i.strip("'") for i in request.form[key].strip("[]'").split(', ')]
                    else:
                        w[key] = request.form[key]
            else:
                i_num = int(key[4:])
                if request.form['list_on'] == 'list_on':
                    list_ = request.form['list']
                    if i_num in w.lists[list_]['cart']:
                        w.lists[list_]['cart'][i_num]['QUANTITY'] += 1
                        w.lists[list_]['cart'][i_num]['PRICE TOTAL'] = (w.lists[list_]['cart'][i_num]['QUANTITY'] *
                                                                        w.lists[list_]['cart'][i_num]['PRICE PER ITEM'])
                        flash = f'Updated {list_}'
                    else:
                        w.add_list(list_, i_num)
                        flash = f'Added to {list_}'
                else:
                    w.add_cart(i_num)
                    flash = 'Added to Cart'
        w.update_cart_size()
    items = w.filter_items()
    w.sort = sort
    w.prev_sort = sort
    try:
        PRODUCTS = sorted([key for key in CATEGORIES[w.cls] if key != 'all'])
    except KeyError:
        PRODUCTS = []
    try:
        TYPES = sorted(CATEGORIES[w.cls][w.product])
    except KeyError:
        TYPES = []

    w.update_self(app.config['USER_DB_PATH'])
    return render_template('search.html', items=items, len_items=len(items), cache=w.cache, nfes=w.nfes, cls=w.cls, product=w.product,
                           types=w.types, sort=w.sort, prev_sort=w.prev_sort, reverse=w.reverse, cart_size=w.cart_size, flash=flash,
                           CACHES=CACHES, NFES=NFES_RNG, CLASS=CLASS, CACHE_NAMES=CACHE_NAMES, HEADER=SEARCH_HEADER, lists=w.lists,
                           PRODUCTS=PRODUCTS, TYPES=TYPES,
                           fp=w.format_price)


@app.route('/cart', methods=['POST', 'GET'])
def cart():
    w = app.config['FIREUSER']
    if request.method == 'POST':
        del_lst = []
        for key in request.form:
            i_num = int(key.split('_')[0])
            if int(request.form[key]) == 0:
                del_lst.append(i_num)
            else:
                w.cart[i_num]['QUANTITY'] = int(request.form[key])
                w.cart[i_num]['PRICE TOTAL'] = w.cart[i_num]['QUANTITY'] * w.cart[i_num]['PRICE PER ITEM']
        if del_lst:
            for i_num in del_lst:
                del w.cart[i_num]
        w.update_cart_size()
    show_cart = w.reorder_snums()
    total_price = w.cart_total_price()
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('cart.html', show_cart=show_cart, CACHES=CACHES, cart_size=w.cart_size,
                           CACHE_NAMES=CACHE_NAMES, HEADER=CART_HEADER, total_price=total_price,
                           fp=w.format_price)


@app.route('/clear_cart')
def clear_cart():
    w = app.config['FIREUSER']
    del_list = [key for key in w.cart]
    for key in del_list:
        del w.cart[key]
    w.update_cart_size()
    return redirect(url_for('cart'))


@app.route('/export', methods=['POST', 'GET'])
def export():
    w = app.config['FIREUSER']
    error = False
    flash = None
    items = []
    if request.method == 'POST':
        if 'cache' in request.form:
            if request.form['cache'] == 'default':
                flash = 'Please Select a Cache'
            else:
                error, flash, items = w.check_cache_items(request.form['cache'])
                w.order_from_cache = request.form['cache']
                if not error:
                    w.fill_cache_info()
                    return redirect(url_for('export_form', download=0))
        else:
            del_lst = []
            for key in request.form:
                if key[:3] == 'cbx':
                    del_lst.append(int(key.split('_')[1]))
            if del_lst:
                for i_num in del_lst:
                    del w.cart[i_num]
            w.update_cart_size()
            w.fill_cache_info()
            return redirect(url_for('export_form', download=0))
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('export.html', items=items, CACHES=CACHES, cart_size=w.cart_size, flash=flash, error=error,
                           CACHE_NAMES=CACHE_NAMES, HEADER=SEARCH_HEADER, err_num_items=f'{len(items)} / {len(w.cart)}',
                           fp=w.format_price)


@app.route('/export_form_<download>', methods=['POST', 'GET'])
def export_form(download):
    w = app.config['FIREUSER']
    show_download = False
    if bool(int(download)):
        o_ref = f"""{'0' * (3 - len(str(w.order_num-1)))}{w.order_num-1}"""
        report, download_name = w.download_order_pdf(o_ref)
        w.update_self(app.config['USER_DB_PATH'])
        return send_file(report, as_attachment=True, download_name=download_name)

    if request.method == 'POST':
        for key in request.form:
            w.report_info[key] = str(request.form[key])
        w.file_order()
        w.reset_variables()
        show_download = True
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('export_form.html', form=w.report_info, CACHES=CACHES, cart_size=w.cart_size, show_download=show_download,
                           CACHE_NAMES=CACHE_NAMES, HEADER=SEARCH_HEADER)


@app.route('/item_<item>', methods=['POST', 'GET'])
def item(item):
    w = app.config['FIREUSER']
    flash = None
    i_num = int(item)
    if request.method == 'POST':
        qty = int(request.form['qty'])
        if qty > 0:
            if request.form['list_on'] == 'list_on':
                list_ = request.form['list']
                if i_num in w.lists[list_]['cart']:
                    w.lists[list_]['cart'][i_num]['QUANTITY'] += qty
                    w.lists[list_]['cart'][i_num]['PRICE TOTAL'] = (w.lists[list_]['cart'][i_num]['QUANTITY'] *
                                                                    w.lists[list_]['cart'][i_num]['PRICE PER ITEM'])
                    flash = f'Updated {list_}'
                else:
                    w.add_list(list_, i_num, qty=qty)
                    flash = f'Added to {list_}'
                w.lists[list_]['total_price'] = w.list_total_price(list_)
                w.lists[list_]['total_qty'] = w.list_total_qty(list_)
            else:
                if i_num in w.cart:
                    w.cart[i_num]['QUANTITY'] += qty
                    w.cart[i_num]['PRICE TOTAL'] = w.cart[i_num]['QUANTITY'] * w.cart[i_num]['PRICE PER ITEM']
                    flash = 'Updated Cart'
                else:
                    w.add_cart(i_num, qty=qty)
                    flash = 'Added to Cart'
        elif qty < 0:
            flash = 'Quantity cannot be negative'
        else:
            flash = 'Please specify a Quantity'
    w.update_cart_size()
    item_info = w.get_item_info(i_num)
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('item.html', item=item, item_info=item_info, CACHES=CACHES, lists=w.lists,
                           cart_size=w.cart_size, CACHE_NAMES=CACHE_NAMES, flash=flash,
                           fp=w.format_price)


@app.route('/orders_<download_xl_all>_<download_xl_by_order>')
def orders(download_xl_all, download_xl_by_order):
    w = app.config['FIREUSER']
    if bool(int(download_xl_all)):
        excel, download_name = w.download_all_by_item_excel()
        return send_file(excel, as_attachment=True, download_name=download_name)
    if bool(int(download_xl_by_order)):
        excel, download_name = w.download_all_by_orders_excel()
        return send_file(excel, as_attachment=True, download_name=download_name)
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('orders.html', orders=w.orders, CACHES=CACHES, cart_size=w.cart_size,
                           CACHE_NAMES=CACHE_NAMES, HEADER=ORDERS_HEADER,
                           fp=w.format_price, fd=w.format_date_time)


@app.route('/order_<order>_<download_pdf>_<download_xl>_<order_again>', methods=['POST', 'GET'])
def order(order, download_pdf, download_xl, order_again):
    flash = None
    w = app.config['FIREUSER']
    if bool(int(download_pdf)):
        report, download_name = w.download_order_pdf(order)
        return send_file(report, as_attachment=True, download_name=download_name)
    if bool(int(download_xl)):
        excel, download_name = w.download_order_excel(order)
        return send_file(excel, as_attachment=True, download_name=download_name)
    if bool(int(order_again)):
        w.order_again(order)
        flash = 'Order Items Added to Cart'
    show_cart = w.orders[order]['cart']
    total_price = w.orders[order]['total_price']
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('order.html', order=order, show_cart=show_cart, CACHES=CACHES, cart_size=w.cart_size, flash=flash,
                           CACHE_NAMES=CACHE_NAMES, HEADER=CART_HEADER, total_price=total_price, date=w.orders[order]['datetime'],
                           fp=w.format_price, fd=w.format_date_time)


@app.route('/lists_<create_new>', methods=['POST', 'GET'])
def lists(create_new):
    w = app.config['FIREUSER']
    flash = None
    create_new = bool(int(create_new))
    if request.method == 'POST':
        l_name = request.form['list_name']
        w.add_new_list(l_name)
        flash = f"""List "{l_name}" added to Lists"""

    w.update_self(app.config['USER_DB_PATH'])
    return render_template('lists.html', lists=w.lists, CACHES=CACHES, cart_size=w.cart_size, create_new=create_new, flash=flash,
                           CACHE_NAMES=CACHE_NAMES, HEADER=LISTS_HEADER,
                           fp=w.format_price, fd=w.format_date_time)


@app.route('/list_<list_>_<order_again>_<delete_list>', methods=['POST', 'GET'])
def list_(list_, order_again, delete_list):
    flash = None
    w = app.config['FIREUSER']
    if bool(int(order_again)):
        w.list_again(list_)
        flash = 'List Items Added to Cart'
    if bool(int(delete_list)):
        del w.lists[list_]
        return redirect(url_for('lists', create_new=0))
    if request.method == 'POST':
        del_lst = []
        for key in request.form:
            i_num = int(key.split('_')[0])
            if int(request.form[key]) == 0:
                del_lst.append(i_num)
            else:
                w.lists[list_]['cart'][i_num]['QUANTITY'] = int(request.form[key])
                w.lists[list_]['cart'][i_num]['PRICE TOTAL'] = (w.lists[list_]['cart'][i_num]['QUANTITY'] *
                                                                w.lists[list_]['cart'][i_num]['PRICE PER ITEM'])
        if del_lst:
            for i_num in del_lst:
                del w.lists[list_]['cart'][i_num]
        w.lists[list_]['total_price'] = w.list_total_price(list_)
        w.lists[list_]['total_qty'] = w.list_total_qty(list_)
    show_cart = w.reorder_list(list_)
    total_price = w.lists[list_]['total_price']
    w.update_self(app.config['USER_DB_PATH'])
    return render_template('list.html', list_=list_, show_cart=show_cart, CACHES=CACHES, cart_size=w.cart_size, flash=flash,
                           CACHE_NAMES=CACHE_NAMES, HEADER=CART_HEADER[1:], total_price=total_price,
                           fp=w.format_price, fd=w.format_date_time)


def open_browser():
    webbrowser.open_new('http://localhost:5000/')


if __name__ == "__main__":
    app.config['USER_DB_PATH'] = make_directory_for_user_db()
    Timer(1, open_browser).start()

    host = '0.0.0.0'
    app.run(host=host, port=5000, debug=False)


