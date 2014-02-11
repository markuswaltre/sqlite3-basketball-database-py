import csv, sqlite3, math

# write to output
file_output = open('output', 'w')

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
c.execute("SELECT count(name), avg(weight), avg(age), avg(experience) FROM player_basics")
stats = c.fetchone()
active_players = stats[0]
avg_weight = stats[1]
avg_age = stats[2]
avg_experience = stats[3]

## Average salary
c.execute("SELECT avg(money) FROM player_salaries WHERE year = '2011-12'")
avg_salary = c.fetchone()[0]

## Average career salary
c.execute("SELECT sum(money) FROM player_salaries")
avg_salary_career = c.fetchone()[0]/active_players

file_output.write('Active players 2011-12:'.ljust(24,' ') + str(active_players) + '\nAverage weight:'.ljust(25,' ') + str(avg_weight) + '\nAverage age:'.ljust(25,' ') + str(avg_age) + '\nAverage experience:'.ljust(25,' ') + str(avg_experience) + '\nAverage salary 2011-12:'.ljust(25,' ') + str(avg_salary) + '\nAverage career salary:'.ljust(25,' ') + str(avg_salary_career))


## Positions
file_output.write('\n\n##### How many play in each position\n')
file_output.write('===========================================\n')
for row in c.execute("SELECT position, count(position) FROM player_stats GROUP BY position"):
    file_output.write('Position: ' + str(row[0]).ljust(5,' ') + '\tCount: ' + str(row[1]) + '\n')
    
## Average money given per year
file_output.write('\n\n##### Average money given, active players and income per year\n')
file_output.write('===========================================\n')
for row in c.execute("SELECT year, sum(money), count(name) FROM player_salaries GROUP BY year"):
    file_output.write(str(row[0]) + '\t' +  str(row[1]).ljust(15,' ') + str(row[2]) + '\t' + str(row[1]/row[2]) + '\n')
    
## Top 10% 2011-12
ten_percent = math.ceil(active_players*0.1)
file_output.write('\n\n##### Top 10 percent earners 2011-12\n')
file_output.write('===========================================\n')
for row in c.execute("SELECT name, money, team FROM player_salaries WHERE year = '2011-12' ORDER BY money desc LIMIT " + str(ten_percent)):
    file_output.write(str(row[0]).ljust(25,' ') + str(row[2]).ljust(25,' ') + str(row[1]) + '\n')
    
## Bottom 10% 2011-12
file_output.write('\n\n##### Bottom 10 percent earners 2011-12\n')
file_output.write('===========================================\n')
for row in c.execute("SELECT name, money, team FROM player_salaries WHERE year = '2011-12' ORDER BY money asc LIMIT 0," + str(ten_percent)):
    file_output.write(str(row[0]).ljust(25,' ') + str(row[2]).ljust(25,' ') + str(row[1]) + '\n')
    
## Middle 50%
file_output.write('\n\n##### Middle 50 percent career earners\n')
file_output.write('===========================================\n')
for row in c.execute("SELECT name, sum(money), team FROM player_salaries GROUP BY name ORDER BY sum(money) desc LIMIT " + str(math.ceil(active_players/4)) + ',' + str(math.ceil(active_players/2))):
    file_output.write(str(row[0]).ljust(25,' ') + str(row[2]).ljust(25,' ') + str(row[1]) + '\n')

## Team statistics
file_output.write('\n\n##### Average salary for team every year and variance\n')
file_output.write('===========================================\n')
file_output.write('===========================================\n\n')

years = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05', '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11', '2011-12']

for x in range(0, len(years)):
    file_output.write('Year ' + years[x] + '\n')
    file_output.write('===========================================')
    max_income = 0
    minimum_income = 100000000
    file_output.write('\n\nTeam'.ljust(25, ' ') + 'Average Salary\n')
    for row in c.execute("SELECT year, team, avg(money) FROM player_salaries WHERE year = '" + years[x] + "' GROUP BY team ORDER BY avg(money)"):
        if row[2] > max_income:
            max_income = row[2]
        if row[2] < minimum_income:
            minimum_income = row[2]
        file_output.write(str(row[1]).ljust(25, ' ') + str(row[2]) + '\n')
    file_output.write('THIS YEARS SALARY VARIANCE: ' + str(max_income - minimum_income) + '\n\n')    
    
## Team statistics
file_output.write('\n\n##### Average age, average experience and variance by season\n')
file_output.write('===========================================\n')
file_output.write('===========================================\n\n')  

for x in range(0, len(years)):
    file_output.write('Year ' + years[x] + '\n')
    file_output.write('===========================================')
    max_exp = 0
    min_exp = 100000000
    file_output.write('\n\nTeam'.ljust(25, ' ') + 'Avg age'.ljust(15, ' ') + 'Avg exp\n')
    for row in c.execute("SELECT avg(player_basics.age), avg(player_basics.experience), player_salaries.team FROM player_basics INNER JOIN player_salaries ON player_basics.name = player_salaries.name WHERE year = '" + years[x] + "' GROUP BY team ORDER BY avg(player_basics.age)"):
        if row[1] > max_exp:
            max_exp = row[1]
        if row[1] < min_exp and min_exp != 0:
            min_exp = row[1]
        file_output.write(str(row[2]).ljust(25, ' ') + str(row[0]).ljust(15, ' ') + str(row[1]) + '\n')
    file_output.write('THIS YEARS EXPERIENCE VARIANCE: ' + str(max_exp - min_exp) + '\n\n')  