-- Insert Users
INSERT INTO Users (username, password_hash, email)
VALUES 
('coach_anna', 'hash_anna', 'anna@example.com'),
('coach_bob', 'hash_bob', 'bob@example.com');

-- Insert Teams
INSERT INTO Teams (name, sport, created_by)
VALUES 
('Falcons', 'Soccer', 2),
('Sharks', 'Basketball', 3);

-- Insert Players
INSERT INTO Players (first_name, last_name, email, phone, team_id)
VALUES 
('John', 'Doe', 'john@example.com', '123-456-7890', 12),
('Jane', 'Smith', 'jane@example.com', '234-567-8901', 12),
('Mike', 'Brown', 'mike@example.com', '345-678-9012', 13),
('Emily', 'White', 'emily@example.com', '456-789-0123', 13);

-- Insert Events
INSERT INTO Events (team_id, event_type, event_date, location)
VALUES 
(12, 'Practice', '2025-05-05 17:00:00', 'Field A'),
(12, 'Game', '2025-05-07 18:00:00', 'Stadium 1'),
(13, 'Practice', '2025-05-06 17:30:00', 'Gym B'),
(13, 'Game', '2025-05-08 19:00:00', 'Arena C');

-- Insert Attendance
INSERT INTO Attendance (event_id, player_id, status)
VALUES 
(20, 7, 'Present'),
(21, 8, 'Absent'),
(22, 9, 'Present'),
(23, 10, 'Present');

-- Insert Matches (only for 'Game' events)
INSERT INTO Matches (event_id, opponent_team, team_score, opponent_score, result)
VALUES 
(21, 'Tigers', 3, 2, 'Win'),
(23, 'Lions', 55, 60, 'Loss');
