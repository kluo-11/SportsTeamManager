-- Insert sample teams
INSERT INTO Teams (name, sport) VALUES ('Team A', 'Soccer');
INSERT INTO Teams (name, sport) VALUES ('Team B', 'Soccer');
INSERT INTO Teams (name, sport) VALUES ('Team C', 'Basketball');
INSERT INTO Teams (name, sport) VALUES ('Team D', 'Basketball');

-- Insert sample events
INSERT INTO Events (team_id, event_type, event_date, location) VALUES
(5, 'Match', '2025-05-05 18:00:00', 'Stadium A'),
(6, 'Match', '2025-05-06 18:00:00', 'Stadium B'),
(7, 'Tournament', '2025-06-10 09:00:00', 'Arena C'),
(8, 'Practice', '2025-05-15 10:00:00', 'Gym D');

