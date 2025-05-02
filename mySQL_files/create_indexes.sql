CREATE INDEX idx_teams_created_by ON Teams(created_by);
CREATE INDEX idx_players_team_id ON Players(team_id);
CREATE INDEX idx_membership_player_team ON Memberships(player_id, team_id);
