from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit, join_room
from flask_cors import CORS
from datetime import datetime
from sqlalchemy.orm import Session
import re

app = Flask(__name__)
app.secret_key = '480e12f5786e79de6991ae64eda54bbc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation des extensions
db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# Modèle des étudiants
class Etudiant(db.Model):
    __tablename__ = 'etudiants'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(50), nullable=False)
    prenom = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    approuve = db.Column(db.Integer, default=0)
    en_ligne = db.Column(db.Boolean, default=False)

class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    sender = db.relationship('Etudiant', foreign_keys=[sender_id])  # Relation avec Etudiant
    receiver_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    receiver = db.relationship('Etudiant', foreign_keys=[receiver_id])  # Optionnel pour le destinataire
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


class HistoriqueLogin(db.Model):
    __tablename__ = 'historique_login'
    id = db.Column(db.Integer, primary_key=True)
    etudiant_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    pseudo = db.Column(db.String(50))
    adresse_ip = db.Column(db.String(45))
    action = db.Column(db.String(10))
    date_connexion = db.Column(db.DateTime)

# Modèle des groupes
class Groupe(db.Model):
    __tablename__ = 'groupes'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)
    group_id = db.Column(db.String(50))
    createur_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    membres = db.relationship('Etudiant', secondary='groupe_membres', backref='groupes')

groupe_membres = db.Table(
    'groupe_membres',
    db.Column('groupe_id', db.Integer, db.ForeignKey('groupes.id'), primary_key=True),
    db.Column('etudiant_id', db.Integer, db.ForeignKey('etudiants.id'), primary_key=True)
)

# Modèle des messages de groupes
class MessageGroupe(db.Model):
    __tablename__ = 'messages_groupe'
    id = db.Column(db.Integer, primary_key=True)
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('etudiants.id'))
    sender = db.relationship('Etudiant', backref='messages_envoyes')
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Création des tables
with app.app_context():
    db.create_all()

# Routes principales
@app.route('/')
def index():
    return redirect(url_for('login'))

# Connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Vérification des identifiants
        if username == 'admin' and password == 'admin123':
            session['loggedin'] = True
            session['id'] = 1
            session['username'] = 'admin'
            return redirect(url_for('admin_page'))

        student = Etudiant.query.filter_by(username=username, password=password).first()
        if student:
            if student.approuve:
                session.update({'loggedin': True, 'id': student.id, 'username': student.username})
                student.en_ligne = True
                db.session.commit()

                # Historique de connexion
                historique = HistoriqueLogin(
                    etudiant_id=student.id,
                    pseudo=student.username,
                    adresse_ip=request.remote_addr,
                    action='login',
                    date_connexion=datetime.utcnow()
                )
                db.session.add(historique)
                db.session.commit()

                return redirect(url_for('chat'))
            else:
                msg = 'Compte non approuvé.'
        else:
            msg = 'Identifiants incorrects.'
    return render_template('login.html', msg=msg)

# Déconnexion
@app.route('/logout')
def logout():
    if 'loggedin' in session:
        student = Etudiant.query.get(session['id'])
        if student:
            student.en_ligne = False
            db.session.commit()

            historique = HistoriqueLogin(
                etudiant_id=student.id,
                pseudo=student.username,
                adresse_ip=request.remote_addr,
                action='logout',
                date_connexion=datetime.utcnow()
            )
            db.session.add(historique)
            db.session.commit()

    session.clear()
    return redirect(url_for('login'))

# Enregistrement
@app.route('/register', methods=['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST':
        form = request.form
        if all(key in form for key in ('nom', 'prenom', 'username', 'password', 'email')):
            username = form['username']
            email = form['email']

            if Etudiant.query.filter_by(username=username).first():
                msg = "Nom d'utilisateur déjà utilisé."
            elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
                msg = "Adresse email invalide."
            else:
                new_user = Etudiant(
                    nom=form['nom'], prenom=form['prenom'], username=username,
                    password=form['password'], email=email
                )
                db.session.add(new_user)
                db.session.commit()
                return redirect(url_for('login'))
        else:
            msg = "Remplissez tous les champs."
    return render_template('register.html', msg=msg)

# Plus d'implémentations disponibles pour le chat, les groupes, et les fonctionnalités admin...


# Route pour la page d'administration
@app.route('/admin')
def admin_page():
    if 'loggedin' in session and session.get('username') == 'admin':
        students_waiting_approval = Etudiant.query.filter_by(approuve=0).all()
        students_all = Etudiant.query.all()
        login_history = HistoriqueLogin.query.join(Etudiant).add_columns(
            Etudiant.username, HistoriqueLogin.pseudo, HistoriqueLogin.adresse_ip,
            HistoriqueLogin.action, HistoriqueLogin.date_connexion
        ).all()

        # Afficher le nombre d'étudiants
        print(f"Etudiants en attente d'approbation : {len(students_waiting_approval)}")
        print(f"Tous les étudiants : {len(students_all)}")
        print(f"Historique des connexions : {len(login_history)}")

        return render_template('admin.html', username=session['username'],
                               students_waiting_approval=students_waiting_approval,
                               students_all=students_all, login_history=login_history)
    return redirect(url_for('login'))

@app.route('/create_group', methods=['POST'])
def create_group():
    if 'loggedin' in session:
        user_id = session['id']
        data = request.json
        nom_groupe = data.get('nom')
        membres = data.get('membres')

        if not nom_groupe or not nom_groupe.strip():
            return jsonify({"message": "Le nom du groupe est obligatoire!"}), 400

        if Groupe.query.filter_by(nom=nom_groupe).first():
            return jsonify({"message": "Ce nom de groupe existe déjà!"}), 400

        groupe = Groupe(nom=nom_groupe.strip(), createur_id=user_id)
        db.session.add(groupe)
        db.session.commit()

        # Ajouter les membres au groupe
        for membre_id in membres:
            etudiant = Etudiant.query.get(membre_id)
            if etudiant:
                groupe.membres.append(etudiant)
        db.session.commit()

        # Retourner la nouvelle liste des groupes
        groups = Groupe.query.all()  # Récupérer tous les groupes
        return jsonify({"message": "Groupe créé avec succès!", "groups": [group.nom for group in groups]}), 200
    return jsonify({"message": "Non autorisé!"}), 401

@app.route('/get_groups')
def get_groups():
    if 'loggedin' in session:
        user_id = session['id']
        student = Etudiant.query.get(user_id)
        
        # Obtenez les groupes auxquels l'étudiant appartient
        groups = student.groupes
        
        return jsonify([{"id": group.id, "nom": group.nom} for group in groups])
    return jsonify({"message": "Non autorisé!"}), 401



@app.route('/get_group_messages/<int:group_id>')
def get_group_messages(group_id):
    if 'loggedin' in session:
        user_id = session['id']
        groupe = Groupe.query.get(group_id)
        
        if not groupe:
            return jsonify({"message": "Groupe introuvable"}), 404
        
        if user_id not in [membre.id for membre in groupe.membres]:
            return jsonify({"message": "Accès interdit à ce groupe"}), 403

        messages = MessageGroupe.query.filter_by(groupe_id=group_id).all()
        return jsonify([{
            'sender_id': msg.sender_id,
            'sender_name': msg.sender.username,  # Ajout du nom d'utilisateur de l'expéditeur
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        } for msg in messages])
    return jsonify([]), 401





# Route pour approuver un étudiant
@app.route('/approve_student/<int:student_id>', methods=['POST'])
def approve_student(student_id):
    student = Etudiant.query.get(student_id)
    if student:
        student.approuve = 1
        db.session.commit()
        return jsonify({"message": "Étudiant approuvé avec succès!"}), 200
    return jsonify({"message": "Étudiant non trouvé!"}), 404

# Route pour rejeter un étudiant
@app.route('/reject_student/<int:student_id>', methods=['POST'])
def reject_student(student_id):
    student = Etudiant.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Étudiant rejeté avec succès!"}), 200
    return jsonify({"message": "Étudiant non trouvé!"}), 404

# Route de banissement
@app.route('/ban_student/<int:student_id>', methods=['POST'])
def ban_student(student_id):
    student = Etudiant.query.get(student_id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({"message": "Étudiant banni!"}), 200
    return jsonify({"message": "Étudiant non trouvé!"}), 404

# Route de chat
@app.route('/chat')
def chat():
    if 'loggedin' in session and 'id' in session:
        user_id = session['id']
        students = Etudiant.query.filter(Etudiant.approuve == 1, Etudiant.id != user_id).all()
        return render_template('chat.html', students=students, user_id=user_id)
    return redirect(url_for('login'))


# Route pour récupérer les messages
@app.route('/get_messages/<int:receiver_id>', methods=['GET'])
def get_messages(receiver_id):
    if 'loggedin' in session:
        user_id = session['id']
        messages = Message.query.filter(
            ((Message.sender_id == user_id) & (Message.receiver_id == receiver_id)) |
            ((Message.sender_id == receiver_id) & (Message.receiver_id == user_id))
        ).order_by(Message.timestamp).all()
        return jsonify([{
            'id': msg.id,
            'sender_id': msg.sender_id,
            'receiver_id': msg.receiver_id,
            'message': msg.message,
            'timestamp': msg.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sender_name': msg.sender.username  # Inclure le nom de l'expéditeur
        } for msg in messages])
    return jsonify([]), 401


# Route pour récupérer les étudiants
@app.route('/get_students', methods=['GET'])
def get_students():
    if 'loggedin' in session:
        user_id = session['id']
        students = Etudiant.query.filter(Etudiant.approuve == 1, Etudiant.id != user_id).all()
        return jsonify([{
            'id': student.id,
            'username': student.username,
            'en_ligne': student.en_ligne
        } for student in students])
    return jsonify([]), 401


# Événement de connexion
@socketio.on('connect')
def handle_connect():
    if 'id' in session:
        student = Etudiant.query.get(session['id'])
        if student:
            student.en_ligne = True
            db.session.commit()

            # Rejoindre les salles des groupes auxquels l'étudiant appartient
            for group in student.groupes:
                join_room(f"group_{group.id}")

            emit('user_status_change', {'id': student.id, 'en_ligne': True}, broadcast=True)


# Événement de déconnexion
@socketio.on('disconnect')
def handle_disconnect():
    if 'id' in session:
        student = Etudiant.query.get(session['id'])
        if student:
            student.en_ligne = False
            db.session.commit()
            emit('user_status_change', {'id': student.id, 'en_ligne': False}, broadcast=True)


# Gestion des événements SocketIO pour le chat
@socketio.on('send_message')
def handle_send_message(data):
    message = Message(sender_id=session['id'], receiver_id=data['receiver_id'], message=data['message'])
    db.session.add(message)
    db.session.commit()

    # Émettre le message dans la salle du destinataire
    emit('receive_message', {
        'sender_id': session['id'],
        'message': data['message'],
        'receiver_id': data['receiver_id'],
        'timestamp': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    }, room=str(data['receiver_id']))  # Utiliser la salle du destinataire

@socketio.on('send_group_message')
def handle_group_socket_message(data):
    group_id = data.get('group_id')
    message = data.get('message')

    if not group_id or not message:
        return emit('error', {'message': 'ID du groupe ou message manquant'}, room=request.sid)

    groupe = Groupe.query.get(group_id)
    if not groupe:
        return emit('error', {'message': 'Groupe introuvable'}, room=request.sid)

    # Vérifiez si l'utilisateur appartient au groupe
    if session['id'] not in [membre.id for membre in groupe.membres]:
        return emit('error', {'message': 'Vous ne faites pas partie de ce groupe'}, room=request.sid)

    # Sauvegarde le message dans la base
    new_message = MessageGroupe(groupe_id=group_id, sender_id=session['id'], message=message)
    db.session.add(new_message)
    db.session.commit()

    # Émettre le message dans la salle du groupe
    emit('group_message', {
        'groupe_id': group_id,
        'message': message,
        'sender_id': session['id'],
        'timestamp': new_message.timestamp.strftime("%Y-%m-%d %H:%M:%S")
    }, room=f"group_{group_id}")

# Exécuter le backend
if __name__ == '__main__':
    socketio.run(app, port=5000, debug=True)
