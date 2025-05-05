CREATE INDEX idx_teams_created_by ON Teams(created_by);
CREATE INDEX idx_players_team_id ON Players(team_id);
CREATE INDEX idx_events_team_id ON Events(team_id);
CREATE INDEX idx_events_event_date ON Events(event_date);
CREATE INDEX idx_events_team_date ON Events(team_id, event_date);
CREATE INDEX idx_matches_event_id ON Matches(event_id);