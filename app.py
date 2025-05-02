from flask import Flask, flash, render_template, request, redirect, url_for
from models import db, Team, Player

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:mypass@localhost/sports_team_manager'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/teams")
def manage_teams():
    teams = Team.query.all()
    return render_template("teams.html", teams=teams)

@app.route("/players")
def manage_players():
    teams = Team.query.all()
    players = Player.query.all()
    return render_template("players.html", teams=teams, players=players)

@app.route('/add_team', methods=['GET', 'POST'])
def add_team():
    if request.method == 'POST':
        # Get form data from the request
        name = request.form['name']
        sport_type = request.form['sport_type']

        # Create a new team
        new_team = Team(name=name, sport_type=sport_type)

        # Add the new team to the database
        db.session.add(new_team)
        db.session.commit()

        # Redirect to the manage_teams page after adding the team
        return redirect(url_for('manage_teams'))

    # For GET request, render the add_team form
    return render_template('add_team.html')

@app.route('/edit_team/<int:team_id>', methods=['GET', 'POST'])
def edit_team(team_id):
    team = Team.query.get_or_404(team_id)

    if request.method == 'POST':
        team.name = request.form['name']
        team.sport_type = request.form['sport_type']

        db.session.commit()
        return redirect(url_for('manage_teams'))

    return render_template('edit_team.html', team=team)

@app.route("/update_team/<int:team_id>", methods=["POST"])
def update_team(team_id):
    team = Team.query.get(team_id)
    if team:
        team.name = request.form["name"]
        team.sport_type = request.form["sport_type"]
        db.session.commit()
    return redirect(url_for("manage_teams"))

@app.route('/delete_team/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)

    db.session.delete(team)
    db.session.commit()

    return redirect(url_for('manage_teams'))

@app.route('/add_player', methods=['GET', 'POST'])
def add_player():
    if request.method == 'POST':
        player_name = request.form['name']
        team_id = request.form['team_id']  # Ensure you are using 'team_id', not 'team'

        # Validate that the team_id is not empty
        if team_id:
            team = Team.query.get(team_id)
            if team:
                new_player = Player(name=player_name, team_id=team_id)
                db.session.add(new_player)
                db.session.commit()
                return redirect(url_for('manage_players'))  # Redirect after POST
            else:
                flash('Invalid team selected', 'danger')
        else:
            flash('Please select a team', 'danger')

    # Fetch all teams for the dropdown
    teams = Team.query.all()
    return render_template('add_player.html', teams=teams)

@app.route('/edit_player/<int:player_id>', methods=['GET', 'POST'])
def edit_player(player_id):
    player = Player.query.get_or_404(player_id)
    teams = Team.query.all()  # Get all teams

    if request.method == 'POST':
        player_name = request.form['name']
        team_id = request.form['team']  # Use 'team' as the form field name

        # Update the player information
        player.name = player_name
        player.team_id = team_id

        db.session.commit()
        return redirect(url_for('manage_players'))  # Redirect after POST

    return render_template('edit_player.html', player=player, teams=teams)

@app.route("/update_player/<int:player_id>", methods=["POST"])
def update_player(player_id):
    player = Player.query.get(player_id)
    if player:
        player.name = request.form["name"]
        player.team_id = request.form["team_id"]
        db.session.commit()
    return redirect(url_for("manage_players"))

@app.route('/delete_player/<int:player_id>', methods=['POST'])
def delete_player(player_id):
    player = Player.query.get_or_404(player_id)

    db.session.delete(player)
    db.session.commit()

    return redirect(url_for('manage_players'))

#player report
@app.route('/players_report', methods=['GET'])
def players_report():
    # Get the selected team from the query string
    team_id = request.args.get('team', type=int)  # Get the team id from the query string

    # If a team is selected, filter players by team; otherwise, show all players
    if team_id:
        players = Player.query.filter_by(team_id=team_id).all()
    else:
        players = Player.query.all()

    # Get the list of all teams to populate the dropdown
    teams = Team.query.all()

    return render_template('players_report.html', players=players, teams=teams)





if __name__ == "__main__":
    app.run(debug=True)
