from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Sample movie data
movies = [
    {
        'id': 1,
        'title': 'Dune: Part Two',
        'genre': 'Sci-Fi/Adventure',
        'duration': '2h 46m',
        'rating': 'PG-13',
        'poster': '🎬',
        'description': 'Paul Atreides unites with Chani and the Fremen while seeking revenge against the conspirators who destroyed his family.'
    },
    {
        'id': 2,
        'title': 'Kung Fu Panda 4',
        'genre': 'Animation/Comedy',
        'duration': '1h 34m',
        'rating': 'PG',
        'poster': '🐼',
        'description': 'Po must train a new warrior to become the next Dragon Warrior while facing a new villain.'
    },
    {
        'id': 3,
        'title': 'Godzilla x Kong',
        'genre': 'Action/Sci-Fi',
        'duration': '1h 55m',
        'rating': 'PG-13',
        'poster': '🦍',
        'description': 'Two ancient titans clash in an epic battle while uncovering the mysteries of Skull Island.'
    },
    {
        'id': 4,
        'title': 'Ghostbusters: Frozen Empire',
        'genre': 'Comedy/Fantasy',
        'duration': '1h 55m',
        'rating': 'PG-13',
        'poster': '👻',
        'description': 'The Spengler family returns to where it all started - the iconic New York City firehouse.'
    }
]

# Showtimes
showtimes = ['10:30 AM', '1:45 PM', '4:30 PM', '7:15 PM', '10:00 PM']

# Sample booked seats (in real app, this would be a database)
bookings = {}

@app.route('/')
def index():
    return render_template('index.html', movies=movies)

@app.route('/movies')
def movie_list():
    return render_template('movies.html', movies=movies)

@app.route('/movie/<int:movie_id>')
def movie_detail(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        return render_template('booking.html', movie=movie, showtimes=showtimes)
    return redirect(url_for('index'))

@app.route('/book/<int:movie_id>', methods=['POST'])
def book_tickets(movie_id):
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if not movie:
        return redirect(url_for('index'))
    
    name = request.form.get('name')
    email = request.form.get('email')
    showtime = request.form.get('showtime')
    tickets = int(request.form.get('tickets', 1))
    seats = request.form.getlist('seats')
    
    # Create booking ID
    booking_id = f"BOOK{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    # Store booking (in real app, save to database)
    bookings[booking_id] = {
        'movie_title': movie['title'],
        'customer_name': name,
        'customer_email': email,
        'showtime': showtime,
        'tickets': tickets,
        'seats': seats,
        'booking_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    flash(f'Booking successful! Your booking ID is: {booking_id}', 'success')
    return redirect(url_for('index'))

@app.route('/confirmation/<booking_id>')
def confirmation(booking_id):
    booking = bookings.get(booking_id)
    if booking:
        return render_template('confirmation.html', booking=booking, booking_id=booking_id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
