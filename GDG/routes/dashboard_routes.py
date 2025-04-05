from flask import Blueprint, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

dashboard_bp = Blueprint('dashboard', __name__)

UPLOAD_FOLDER = 'uploads/shared_spaces'

@dashboard_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@dashboard_bp.route('/share-space', methods=['POST'])
def share_space():
    if 'space_image' in request.files:
        image = request.files['space_image']
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))

    # You can later store these in your database
    height = request.form['height']
    width = request.form['width']
    max_weight = request.form['max_weight']
    route = request.form['route']
    estimated_cost = request.form['estimated_cost']

    print(f"Shared: {height}, {width}, {max_weight}, {route}, ₹{estimated_cost}")
    return redirect(url_for('dashboard.dashboard'))
