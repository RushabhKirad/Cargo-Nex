from flask import Flask, render_template, request, redirect, url_for
from routes.dashboard_routes import dashboard_bp
import os

# Flask App Initialization
app = Flask(__name__, static_folder='static', template_folder='templates')

# Upload Folder Setup
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Register Blueprints
app.register_blueprint(dashboard_bp)

# Routes
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/vehicle-registration', methods=['GET', 'POST'])
def vehicle_registration():
    if request.method == 'POST':
        vehicle_number = request.form['vehicle_number']
        vehicle_type = request.form['vehicle_type']

        fitness_certificate = request.files.get('fitness_certificate')
        puc_certificate = request.files.get('puc_certificate')
        permit = request.files.get('permit')

        if fitness_certificate:
            fitness_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], fitness_certificate.filename))
        if puc_certificate:
            puc_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], puc_certificate.filename))
        if permit:
            permit.save(os.path.join(app.config['UPLOAD_FOLDER'], permit.filename))

        return redirect(url_for('dashboard'))

    return render_template('vehicle_registration.html')

@app.route('/dashboard')
def dashboard():
    # Placeholder stats for now – later replace with DB data
    stats = {
        "total_vehicles": 128,
        "active_deliveries": 32,
        "avg_fuel_efficiency": "7.8 km/l",
        "shared_options": 6,
        "shared_space": [
            {
                "route": "Pune ➝ Nashik",
                "height": "5ft",
                "breadth": "4ft",
                "weight": "300 kg",
                "cost": "₹3,200",
                "image": "images/empty-space.jpg"
            }
        ]
    }
    return render_template('dashboard.html', stats=stats)

@app.route('/tracking')
def tracking():
    return render_template('tracking.html')

# Prevent Caching for Latest Loads
@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# Run the Flask App
if __name__ == '__main__':
    app.run(debug=True)
