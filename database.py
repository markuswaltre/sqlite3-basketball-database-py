import csv, sqlite3, math

# write to output
file_output = open('output', 'w')
file_output.write('hi there\n')

# csv reader
players = csv.reader(open("input/playerStats.csv"))
salaries = csv.reader(open("input/playerSalaries.csv"))
conn = sqlite3.connect(":memory:")
conn.text_factory = str
c = conn.cursor()


#### String for headers
super_long_string = "name, weight, height, positions, hand, experience, age, year, age_2012, team, league, position, games, games_started, minutes_played, field_goals, field_goals_attempted, field_goals_percentage, three_point_field_goals, three_point_field_goals_attempted, three_point_field_goals_percentage, two_point_field_goals, two_point_field_goals_attempts, two_point_field_goals_percentage, free_throws, free_throws_attempted, free_throw_percentage, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points"

#### Strings for the extracted headers
player_basics = "name, weight, height, positions, hand, experience, age"
player_stats = "name, year, age_2012, team, league, position, games, games_started, minutes_played, field_goals, field_goals_attempted, field_goals_percentage, three_point_field_goals, three_point_field_goals_attempted, three_point_field_goals_percentage, two_point_field_goals, two_point_field_goals_attempts, two_point_field_goals_percentage, free_throws, free_throws_attempted, free_throw_percentage, offensive_rebounds, defensive_rebounds, total_rebounds, assists, steals, blocks, turnovers, personal_fouls, points"

player_salaries = "name, year, team, money"

#### Everything table
c.execute("CREATE TABLE everything(" + super_long_string + ", yada)")
c.executemany("INSERT INTO everything(" + super_long_string + ", yada) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", players)

#### Player tables
c.execute("CREATE TABLE player_basics AS SELECT DISTINCT " + player_basics + " FROM everything")
c.execute("CREATE TABLE player_stats AS SELECT " + player_stats + " FROM everything")
c.execute("DELETE FROM player_stats WHERE team = 'TOT'")

#### Salaries table (integer is there so you can sort on money)
c.execute("CREATE TABLE player_salaries(" + player_salaries + " integer, yada)")
c.executemany("INSERT INTO player_salaries(" + player_salaries + ", yada) VALUES (?, ?, ?, ?, ?);", salaries)

## Basic generated stats : players, weight, age
c.execute("SELECT count(name), avg(weight), avg(age) FROM player_basics")
stats = c.fetchone()
active_players = stats[0]
avg_weight = stats[1]
avg_age = stats[2]

## Positions
for row in c.execute("SELECT position, count(position) FROM player_stats GROUP BY position"):
    pos1 = row[0], 
    pos2 = row[1]
    
    
## Top 10%
ten_percent = math.ceil(active_players*0.1)
for row in c.execute("SELECT name, money, team FROM player_salaries WHERE year = '2011-12' ORDER BY money desc LIMIT " + str(ten_percent)):
    pos = row
    
## Bottom 10%
for row in c.execute("SELECT name, money, team FROM player_salaries WHERE year = '2011-12' ORDER BY money asc LIMIT 0," + str(ten_percent)):
    pos = row

    





