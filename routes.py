import os
from flask import render_template, redirect, request, url_for, flash, current_app 
from werkzeug.utils import secure_filename
# from models import Survey, Option
from app import app, db
from models import User, Contact, House, Booking
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm, ContactForm, AddHouseForm, BookingForm


@app.route('/')
def main():
    houses = House.query.all()
    form = BookingForm()
    return render_template('index.html', form=form, houses=houses)
                          
@app.route('/add_house', methods = ['GET', 'POST'])
@login_required
def add():
    if not current_user.is_admin:
        flash('Ви не маєте дозволу на доступ до цієї сторінки.','danger')
        return redirect(url_for('main'))
    form = AddHouseForm()
    if form.validate_on_submit():
        if form.image.data:
            image_file = secure_filename(form.image.data.filename)
            image_path = os.path.join(current_app.root_path, 'static/images', image_file)
            form.image.data.save(image_path)
        else:
            image_file = 'default.png'
        new_house = House(
            name = form.name.data,
            country = form.country.data,
            address = form.address.data,
            description = form.description.data,
            residents = form.residents.data,
            price = form.price.data,
            image = image_file
        )
        db.session.add(new_house)
        db.session.commit()
        flash('Нове житло додане!', 'success')
        return redirect(url_for('main'))
    return render_template('add_house.html', form=form)

@app.route('/edit/<int:house_id>', methods = ['GET', 'POST'])
@login_required
def edit(house_id):
    if not current_user.is_admin:
        flash('Ви не маєте дозволу на доступ до цієї сторінки.', 'danger')
        return redirect(url_for('main'))
    house = House.query.get_or_404(house_id)
    form = AddHouseForm(obj = house)
    if form.validate_on_submit():
        house.name = form.name.data
        house.country = form.country.data
        house.address = form.address.data
        house.description = form.description.data
        house.residents = form.residents.data
        house.price = form.price.data
        db.session.commit()
        flash('Зміни успішно збережені', 'success')
        return redirect(url_for('main'))
    return render_template('edit.html', house=house, form=form)


@app.route('/delete/<int:house_id>', methods = ['POST'])
@login_required
def delete(house_id):
    if not current_user.is_admin:
        flash('Ви не маєте дозволу на доступ до цієї сторінки.', 'danger')
        return redirect(url_for('main'))
    house_delete = House.query.get_or_404(house_id)
    db.session.delete(house_delete)
    db.session.commit()
    flash('Місце проживання успішно видалене', 'success')
    return redirect(url_for('main'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('Ви не маєте дозволу на доступ до цієї сторінки.', 'danger')
        return redirect(url_for('main'))
    users = User.query.all()
    return render_template('dashboard.html', users=users)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256')
        new_user = User(username=form.username.data, password=hashed_password, country = form.country.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Реєстрація успішна! Тепер ви можете увійти.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form) 

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Ви ввійшли в аккаунт', 'success')
            return redirect(url_for('main'))
    return render_template('login.html', form=form)

@app.route('/booking/<int:house_id>', methods=['GET', 'POST'])
@login_required
def booking(house_id):
    form = BookingForm()
    house = House.query.get_or_404(house_id)
    if form.validate_on_submit():
        if form.arrival_residents.data > house.residents:
            flash('Кількість жителів не може бути більшою, ніж задана на сайті власником', 'danger')
            return redirect(url_for('main'))
        arrival_date = form.arrival_date.data
        departure_date = form.departure_date.data
        existing_booking = Booking.query.filter(Booking.house_id == house_id or Booking.arrival_date == arrival_date or Booking.departure_date == departure_date or Booking.arrival_date == departure_date or Booking.departure_date == arrival_date ).first()
        if existing_booking:
            flash('Це житло вже заброньоване на обрані дати', 'danger')
            return redirect(url_for('main'))
        print(f"House ID: {house.id}")
        books = Booking(house_id = house.id, user_id = current_user.id, booking_name = form.booking_name.data, arrival_date = form.arrival_date.data, departure_date = form.departure_date.data, arrival_residents = form.arrival_residents.data)
        house.status = 'заброньовано'
        db.session.add(books)
        db.session.commit()
        flash('Бронювання здійснено успішно', 'success')
        return redirect(url_for('main'))
    else:
        print("Помилки валідації:", form.errors)
    return render_template('index.html', form=form, house=house)

@app.route('/full_house/<int:house_id>')
def full_house(house_id):
    ful_house = House.query.get_or_404(house_id)
    return render_template('full_house.html', ful_house=ful_house)


@app.route('/logout')
def logout():
    logout_user()
    flash('Ви вийшли з аккаунта', 'success')
    return redirect(url_for('main'))

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        new_contact = Contact(name = form.name.data, email = form.email.data, message = form.message.data)
        db.session.add(new_contact)
        db.session.commit()
        flash("Повідомлення успішно надіслано. Дякую за фідбек.", 'success')
        return redirect(url_for('main'))
    return render_template('contact.html', form=form)

# @app.route('/admin')
# @login_required
# def admin():
#     if not current_user.is_admin:
#         flash('Ви не маєте дозволу на доступ до цієї сторінки.', 'danger')
#         return redirect(url_for('main'))
#     return render_template('admin.html')

@app.route('/toggle_admin/<int:user_id>', methods = ['GET', 'POST'])
@login_required
def toggle_admin(user_id):
    if not current_user.is_admin:
        flash('Ви не маєте дозволу на доступ до цієї сторінки.', 'danger')
        return redirect(url_for('dashboard'))
    
    user = User.query.get_or_404(user_id)

    user.is_admin = not user.is_admin
    db.session.commit()

    if user.is_admin:
        flash(f"Користувач {user.username} отримав права адміністратора.", 'success' )
        return redirect(url_for('dashboard'))
    else:
        flash(f"У користувача {user.username} було скасовано права адміністратора", 'success')
        return redirect(url_for('dashboard'))

@app.route('/about')
def about():
    return render_template('about.html')


