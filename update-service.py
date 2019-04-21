import mysql.connector
from mysql.connector.cursor import MySQLCursorPrepared
import math
import urllib.request
import aux.config as config
import datetime
import os

def get_data(cursor,max_matchday,maxsumcum,league,league_num):
    cursor.execute(
        'SELECT season, matchday FROM football_germany where league=' + str(league_num) + ' order by season desc, matchday desc limit 1;')
    result = cursor.fetchall()
    last_matchday = result[0][1]
    last_season = result[0][0]
    if last_matchday == max_matchday:
        actual_matchday = 1
        last_season_num = last_season.split('-')
        last_season_num = int(last_season_num[0]) + 1
        actual_season = str(last_season_num) + '-' + str(
            (last_season_num + 1) - math.floor((last_season_num + 1) / 100) * 100)
    else:
        actual_matchday = last_matchday + 1
        try:
            actual_season = last_season.decode()
        except:
            actual_season = last_season


    if league_num == 1 or league_num == 2:
        f = urllib.request.urlopen(
            'https://www.kicker.de/news/fussball/bundesliga/spieltag/' + league + '/' + actual_season + '/' + str(actual_matchday) + '/0/spieltag.html')
    else:
        f = urllib.request.urlopen(
            'https://www.kicker.de/news/fussball/3liga/spieltag/' + league + '/' + actual_season + '/' + str(actual_matchday) + '/0/spieltag.html')

    print('Working ' + league + ' on season ' + actual_season + ' matchday ' + str(actual_matchday))

    total_data = [[None for _ in range(9)] for _ in range(maxsumcum)]

    myfile = f.read()

    myfile = str(myfile).split('\\r\\n')
    str2find = '<td class="alignleft nowrap" >'

    indices = [i for i, s in enumerate(myfile) if str2find in s]

    sumcum_i = 0
    i_cont = 0

    if len(indices)!=maxsumcum:
        total_data = None
        print('Matchday not done')
    else:
        for i in enumerate(indices):

            if sumcum_i < maxsumcum:
                # result
                try:
                    idx = myfile[indices[i[0]]].find(':')
                    res_final = myfile[indices[i[0]]][idx - 1:idx + 2]
                    res_final = res_final.split(':')
                    res_final = [int(x) for x in res_final]
                except:
                    res_final = [None, None]
                try:
                    idx = myfile[indices[i[0]]].find('(')
                    res_half = myfile[indices[i[0]]][idx + 1:idx + 4]
                    res_half = res_half.split(':')
                    res_half = [int(x) for x in res_half]
                except:
                    res_half = [None, None]

                # team names
                idx = myfile[indices[i[0]] - 18].find(actual_season + '/') + len(actual_season + '/')
                home_team = myfile[indices[i[0]] - 18][idx:]
                idx = home_team.find('/')
                home_team = home_team[0:idx]
                idx = home_team.rfind('-')
                home_team = home_team[0:idx]

                idx = myfile[indices[i[0]] - 7].find(actual_season + '/') + len(actual_season + '/')
                visitor_team = myfile[indices[i[0]] - 7][idx:]
                idx = visitor_team.find('/')
                visitor_team = visitor_team[0:idx]
                idx = visitor_team.rfind('-')
                visitor_team = visitor_team[0:idx]

                # inserting data into the final list
                total_data[i_cont][0] = home_team
                total_data[i_cont][1] = visitor_team
                total_data[i_cont][2] = res_final[0]
                total_data[i_cont][3] = res_final[1]
                total_data[i_cont][4] = res_half[0]
                total_data[i_cont][5] = res_half[1]
                total_data[i_cont][6] = actual_season
                total_data[i_cont][7] = actual_matchday
                total_data[i_cont][8] = league_num

                # updating indexs
                i_cont += 1
                sumcum_i += 1

    return total_data


## main

# read configuration
[host_config,user_config, password_config, dbname, port, engine] = config.read()

# connection
print('opening db connection')
connection = mysql.connector.connect(host=host_config,
                        database=dbname,
                        user=user_config,
                        password=password_config,
                        use_pure=True)
cursor = connection.cursor(cursor_class=MySQLCursorPrepared)

sql_insert_query = """ INSERT INTO `football_germany`
                          (`home`,`visitor`,`goals_home`,`goals_visitor`,`goals_home_half`,`goals_visitor_half`,`season`,`matchday`,`league`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""

# logfile
logfile = [None]*3

# 1-bundesliga
max_matchday = 34
maxsumcum = 9
league = '1-bundesliga'
league_num = 1
try:
    total_data_1 = get_data(cursor,max_matchday,maxsumcum,league,league_num)
    if total_data_1!=None:
        result = cursor.executemany(sql_insert_query, total_data_1)
        connection.commit()
        logfile[0] = '1-bundesliga results worked right on ' + str(datetime.datetime.now())
    else:
        logfile[0] = '1-bundesliga: matchday was not done on ' + str(datetime.datetime.now())

except mysql.connector.Error as error_1:
    print('Error getting 1-bundesliga ' + str(error_1))
    logfile[0] = 'Error getting 1-bundesliga ' + str(error_1) + str(datetime.datetime.now())

# 2-bundesliga
max_matchday = 34
maxsumcum = 9
league = '2-bundesliga'
league_num = 2
try:
    total_data_2 = get_data(cursor, max_matchday, maxsumcum, league, league_num)
    if total_data_2 != None:
        result = cursor.executemany(sql_insert_query, total_data_2)
        connection.commit()
        logfile[1] = '2-bundesliga results worked right on ' + str(datetime.datetime.now())
    else:
        logfile[1] = '2-bundesliga: matchday was not done on ' + str(datetime.datetime.now())

except mysql.connector.Error as error_2:
    print('Error getting 2-bundesliga ' + str(error_2))
    logfile[1] = 'Error getting 2-bundesliga ' + str(error_2) + str(datetime.datetime.now())

# 3-liga
max_matchday = 38
maxsumcum = 10
league = '3-liga'
league_num = 3
try:
    total_data_3 = get_data(cursor,max_matchday,maxsumcum,league,league_num)
    if total_data_3 != None:
        result = cursor.executemany(sql_insert_query, total_data_3)
        connection.commit()
        logfile[2] = '3-liga results worked right on ' + str(datetime.datetime.now())
    else:
        logfile[2] = '3-liga: matchday was not done on ' + str(datetime.datetime.now())

except mysql.connector.Error as error_3:
    print('Error getting 3-liga reuslts: {}'.format(error_3))
    logfile[2] = 'Error getting 3-liga ' + str(error_3) + str(datetime.datetime.now())

# closing connection
print('closing db connection')
connection.close()

# create logfile
print('creating logfile')
cwd = os.getcwd()
logfilePath = os.path.join(cwd, 'logfile')
if os.path.isdir(logfilePath)==False:
    os.mkdir(logfilePath)

file_name = 'logfile_' + datetime.datetime.now().strftime('%Y%m%d%H%M%S') + '.txt'
logfile_raw= open(os.path.join(logfilePath, file_name),'w+')
for row in logfile:
    logfile_raw.write(row)
    logfile_raw.write('\n')
logfile_raw.close()

print('done')
