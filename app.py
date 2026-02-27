from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ======= DATABASE MODELS =======
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.String(200), nullable=False)
    project_link = db.Column(db.String(200), nullable=True)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    message = db.Column(db.Text, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# ==================== PUBLIC ROUTES ====================

@app.route('/')
def home():
    projects = Project.query.all()
    return render_template('home.html', projects=projects)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/projects')
def projects_page():
    projects = Project.query.all()
    return render_template('projects.html', projects=projects)

@app.route('/resume')
def resume():
    return render_template('resume.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip()
        message_text = request.form['message'].strip()
        # Server-side validation
        if len(name) < 2 or '@' not in email or len(message_text) < 10:
            flash('Please fill out the form correctly.', 'danger')
            return redirect(url_for('contact'))
        new_message = Message(name=name, email=email, message=message_text)
        db.session.add(new_message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html')

# ==================== ADMIN ROUTES ====================

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        admin = User.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            flash('Logged in successfully!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid credentials', 'danger')
            return redirect(url_for('admin_login'))
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin_id', None)
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_login'))
    projects = Project.query.all()
    return render_template('admin_dashboard.html', projects=projects)

@app.route('/admin/project/add', methods=['GET', 'POST'])
def add_project():
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_login'))
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        image_url = request.form['image_url']
        project_link = request.form['project_link']
        new_project = Project(title=title, description=description, image_url=image_url, project_link=project_link)
        db.session.add(new_project)
        db.session.commit()
        flash('Project added successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_project.html')

@app.route('/admin/project/edit/<int:id>', methods=['GET', 'POST'])
def edit_project(id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_login'))
    project = Project.query.get_or_404(id)
    if request.method == 'POST':
        project.title = request.form['title']
        project.description = request.form['description']
        project.image_url = request.form['image_url']
        project.project_link = request.form['project_link']
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('edit_project.html', project=project)

@app.route('/admin/project/delete/<int:id>')
def delete_project(id):
    if 'admin_id' not in session:
        flash('Please login first!', 'danger')
        return redirect(url_for('admin_login'))
    project = Project.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('admin_dashboard'))

# ==================== RUN SERVER ====================

if __name__ == '__main__':
    app.run(debug=True)
