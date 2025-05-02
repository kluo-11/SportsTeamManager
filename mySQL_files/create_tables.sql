CREATE TABLE Users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL
);

CREATE TABLE Teams (
    team_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sport VARCHAR(255) NOT NULL,
    created_by INT,
    FOREIGN KEY (created_by) REFERENCES Users(user_id)
);

CREATE TABLE Players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    phone VARCHAR(255),
    team_id INT,
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Memberships (
    membership_id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT,
    team_id INT,
    role VARCHAR(255),
    FOREIGN KEY (player_id) REFERENCES Players(player_id),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Events (
    event_id INT AUTO_INCREMENT PRIMARY KEY,
    team_id INT,
    event_type VARCHAR(255),
    event_date DATETIME,
    location VARCHAR(255),
    FOREIGN KEY (team_id) REFERENCES Teams(team_id)
);

CREATE TABLE Attendance (
    attendance_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT,
    player_id INT,
    status VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES Events(event_id),
    FOREIGN KEY (player_id) REFERENCES Players(player_id)
);

CREATE TABLE Matches (
    match_id INT AUTO_INCREMENT PRIMARY KEY,
    event_id INT,
    opponent_team VARCHAR(255) NOT NULL,
    team_score INT,
    opponent_score INT,
    result VARCHAR(255),
    FOREIGN KEY (event_id) REFERENCES Events(event_id)
);
