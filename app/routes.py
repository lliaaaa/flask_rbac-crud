from flask import Blueprint, request, redirect, url_for,flash, render_template
from .models import db, Record
from .decorators import login_required, role_required


bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    return render_template("home.html")

# --- View (Read) ---
@bp.route('/dashboard')
@login_required
def dashboard():
    records = Record.query.all()
    return render_template('dashboard.html', records=records)

# --- Create Route ---
@bp.route('/add', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        name = request.form['name'].strip()
        program = request.form['program'].strip()
        year = request.form['year'].strip()
        course = request.form['course'].strip()

        # --- Validation ---
        if not name or not program or not year or not course:
            flash('All fields are required!')
            return redirect(url_for('add_record'))

        if any(char.isdigit() for char in name) or any(char.isdigit() for char in program) or any(char.isdigit() for char in course):
            flash('Name, Program, and Course should not contain numbers!')
            return redirect(url_for('add_record'))

        if not year.isdigit():
            flash('Year must be a number!')
            return redirect(url_for('add_record'))

        new_record = Record(name=name, program=program, year=int(year), course=course)
        db.session.add(new_record)
        db.session.commit()
        flash('Record added successfully!')
        return redirect(url_for('main.dashboard'))

    return render_template('add.html')

# --- Update Route ---
@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_record(id):
    record = Record.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form['name'].strip()
        program = request.form['program'].strip()
        year = request.form['year'].strip()
        course = request.form['course'].strip()

        # --- Validation ---
        if not name or not program or not year or not course:
            flash('All fields are required!')
            return redirect(url_for('edit_record', id=id))

        if any(char.isdigit() for char in name) or any(char.isdigit() for char in program) or any(char.isdigit() for char in course):
            flash('Name, Program, and Course should not contain numbers!')
            return redirect(url_for('edit_record', id=id))

        if not year.isdigit():
            flash('Year must be a number!')
            return redirect(url_for('edit_record', id=id))

        record.name = name
        record.program = program
        record.year = int(year)
        record.course = course
        db.session.commit()
        flash('Record updated successfully!')
        return redirect(url_for('main.dashboard'))

    return render_template('edit.html', record=record)

# --- Delete Route ---
@bp.route('/delete/<int:id>')
def delete_record(id):
    record = Record.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    flash('Record deleted successfully!')
    return redirect(url_for('main.dashboard'))