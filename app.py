from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, User, Team, Player, Membership, Event, Attendance, Match
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypass@localhost/sports_team_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'dev'  # Replace for production

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# ----------- TEAMS ------------

@app.route('/teams')
def manage_teams():
    teams = Team.query.all()
    return render_template('teams.html', teams=teams)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        name = request.form['name']
        sport = request.form['sport']
        created_by = request.form.get('created_by', 1)  # Placeholder user

        team = Team(name=name, sport=sport, created_by=created_by)
        db.session.add(team)
        db.session.commit()
        return redirect(url_for('manage_teams'))
    return render_template('add_team.html')

@app.route('/edit_team/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)
    if request.method == 'POST':
        team.name = request.form['name']
        team.sport = request.form['sport']
        db.session.commit()
        return redirect(url_for('manage_teams'))
    return render_template('edit_team.html', team=team)

@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
    db.session.delete(team)
    db.session.commit()
    return redirect(url_for('manage_teams'))

# ----------- PLAYERS & MEMBERSHIPS ------------

@app.route('/players')
def manage_players():
    players = Player.query.all()
    teams = Team.query.all()
    memberships = Membership.query.all()
    return render_template('players.html', players=players, teams=teams, memberships=memberships)

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    teams = Team.query.all()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        team_id = request.form['team_id']
        role = request.form['role']

        player = Player(first_name=first_name, last_name=last_name, email=email, phone=phone)
        db.session.add(player)
        db.session.commit()

        membership = Membership(player_id=player.player_id, team_id=team_id, role=role)
        db.session.add(membership)
        db.session.commit()

        return redirect(url_for('manage_players'))

    return render_template('add_player.html', teams=teams)

@app.route('/edit_player/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    membership = Membership.query.filter_by(player_id=player_id).first()
    teams = Team.query.all()

    if request.method == 'POST':
        player.first_name = request.form['first_name']
        player.last_name = request.form['last_name']
        player.email = request.form['email']
        player.phone = request.form['phone']
        membership.team_id = request.form['team_id']
        membership.role = request.form['role']
        db.session.commit()
        return redirect(url_for('manage_players'))

    return render_template('edit_player.html', player=player, membership=membership, teams=teams)

@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)
    Membership.query.filter_by(player_id=player_id).delete()
    db.session.delete(player)
    db.session.commit()
    return redirect(url_for('manage_players'))

# ----------- REPORT ------------

'''@app.route('/players_report')
def players_report():
    team_id = request.args.get('team', type=int)
    teams = Team.query.all()

    if team_id:
        memberships = Membership.query.filter_by(team_id=team_id).all()
        player_ids = [m.player_id for m in memberships]
        players = Player.query.filter(Player.player_id.in_(player_ids)).all()
    else:
        players = Player.query.all()

    return render_template('players_report.html', players=players, teams=teams)
'''

# ----------- SCHEDULE ------------

@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    teams = Team.query.all()
    filtered_schedule = []

    if request.method == 'POST':
        team_id = request.form.get('team')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')

        query = text("""
            -- Events
            SELECT 
                e.event_type AS type,
                t.name AS team_name,
                e.event_date AS date,
                e.location AS location,
                NULL AS opponent,
                NULL AS team_score,
                NULL AS opponent_score,
                NULL AS result
            FROM Events e
            JOIN Teams t ON e.team_id = t.team_id
            WHERE (:team_id IS NULL OR e.team_id = :team_id)
              AND (:start_date IS NULL OR e.event_date >= :start_date)
              AND (:end_date IS NULL OR e.event_date <= :end_date)

            UNION

            -- Matches
            SELECT 
                'Match' AS type,
                t.name AS team_name,
                e.event_date AS date,
                e.location AS location,
                m.opponent_team AS opponent,
                m.team_score AS team_score,
                m.opponent_score AS opponent_score,
                m.result AS result
            FROM Matches m
            JOIN Events e ON m.event_id = e.event_id
            JOIN Teams t ON e.team_id = t.team_id
            WHERE (:team_id IS NULL OR e.team_id = :team_id)
              AND (:start_date IS NULL OR e.event_date >= :start_date)
              AND (:end_date IS NULL OR e.event_date <= :end_date)

            ORDER BY date ASC
        """)

        filtered_schedule = db.session.execute(query, {
            'team_id': team_id or None,
            'start_date': start_date or None,
            'end_date': end_date or None
        }).fetchall()

    return render_template('schedule.html', teams=teams, filtered_schedule=filtered_schedule)

@app.route('/manage_schedule', methods=['GET', 'POST'])
def manage_schedule():
    teams = Team.query.all()

    if request.method == 'POST':
        # Retrieve common event fields
        team_id = request.form.get('team_id')
        event_type = request.form.get('event_type')
        event_date = request.form.get('event_date')
        location = request.form.get('location')
        is_match = request.form.get('is_match')

        # Insert the event
        new_event = Event(team_id=team_id, event_type=event_type, event_date=event_date, location=location)
        db.session.add(new_event)
        db.session.flush()  # Get event_id before commit

        if is_match:
            opponent = request.form.get('opponent_team')
            team_score = request.form.get('team_score')
            opponent_score = request.form.get('opponent_score')
            result = request.form.get('result')

            match = Match(
                event_id=new_event.event_id,
                opponent_team=opponent,
                team_score=team_score,
                opponent_score=opponent_score,
                result=result
            )
            db.session.add(match)

        db.session.commit()
        return redirect(url_for('manage_schedule'))

    # Retrieve all events + matches
    schedule = db.session.execute(text("""
        SELECT 
            e.event_id,
            t.name AS team_name,
            e.event_type,
            e.event_date,
            e.location,
            m.opponent_team,
            m.team_score,
            m.opponent_score,
            m.result
        FROM Events e
        JOIN Teams t ON e.team_id = t.team_id
        LEFT JOIN Matches m ON e.event_id = m.event_id
        ORDER BY e.event_date DESC
    """)).fetchall()

    return render_template('manage_schedule.html', teams=teams, schedule=schedule)

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)
    match = Match.query.filter_by(event_id=event_id).first()
    teams = Team.query.all()

    if request.method == 'POST':
        event.team_id = request.form['team_id']
        event.event_type = request.form['event_type']
        event.event_date = request.form['event_date']
        event.location = request.form['location']

        is_match = request.form.get('is_match')

        if is_match and not match:
            match = Match(event_id=event.event_id)
            db.session.add(match)

        if is_match:
            match.opponent_team_name = request.form['opponent_team_name']
            match.team_score = request.form['team_score']
            match.opponent_score = request.form['opponent_score']
            match.result = request.form['result']
        elif match:
            db.session.delete(match)

        db.session.commit()
        return redirect(url_for('manage_schedule'))

    return render_template('edit_event.html', event=event, match=match, teams=teams)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    event = Event.query.get_or_404(event_id)
    match = Match.query.filter_by(event_id=event_id).first()

    if match:
        db.session.delete(match)
    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('manage_schedule'))


# ----------- LAUNCH ------------

if __name__ == '__main__':
    app.run(debug=True)
