import urllib.request
import math
import csv

# 2-bundesliga
# 1981-1994 --> 20 teams
# 1992 --> 24 teams
# 1995 >= 18 teams


liga = '1-bundesliga'

if liga == '1-bundesliga':
    num_matches = 9
    season_list = list(range(1965, 2018))
    matchday_list = list(range(1, 35))
    liga_num = 1
    maxsumcum = 9
elif liga == '3-liga':
    num_matches = 10
    season_list = list(range(2008, 2018))
    matchday_list = list(range(1, 39))
    liga_num = 3
    maxsumcum = 10
else:
    num_matches = 10
    season_list = list(range(1981, 2018))
    matchday_list = list(range(1, 39))
    liga_num = 2
    maxsumcum = 9

total_data = [[None for _ in range(9)] for _ in range(len(season_list)*(len(matchday_list))*num_matches)]
i_cont = 0


for actual_season in season_list:
    # 2-bundesliga exceptions
    if actual_season==1992 and liga=='2-bundesliga':
        matchday_list = list(range(1, 47))
        maxsumcum = 12
    elif actual_season>=1995 and liga=='2-bundesliga':
        matchday_list = list(range(1, 35))
        maxsumcum = 9
    elif actual_season<1995 and liga=='2-bundesliga':
        matchday_list = list(range(1, 39))
        maxsumcum = 10

    for matchday in matchday_list:

        str_temp = (actual_season + 1) - math.floor((actual_season+1)/100)*100
        if str_temp<10:
            str_temp = '0' + str(str_temp)
        else:
            str_temp = str(str_temp)

        season = str(actual_season) + '-' + str_temp

        if liga=='3-liga':
            f = urllib.request.urlopen('https://www.kicker.de/news/fussball/3liga/spieltag/' + liga + '/' + season + '/' + str(matchday) + '/0/spieltag.html')
        else:
            f = urllib.request.urlopen('https://www.kicker.de/news/fussball/bundesliga/spieltag/' + liga + '/' + season + '/' + str(matchday) + '/0/spieltag.html')

        print('Working on season ' + season + ' matchday ' + str(matchday) + '. checksum: ' + str(sum(x is not None for x in [i[2] for i in total_data]) -i_cont))
        myfile = f.read()

        myfile = str(myfile).split('\\r\\n')
        str2find = '<td class="alignleft nowrap" >'

        indices = [i for i, s in enumerate(myfile) if str2find in s]

        sumcum_i = 0
        for i in enumerate(indices):

            if sumcum_i < maxsumcum:
                # result
                try:
                    idx = myfile[indices[i[0]]].find(':')
                    res_final = myfile[indices[i[0]]][idx-1:idx+2]
                    res_final = res_final.split(':')
                    res_final = [int(x) for x in res_final]
                except:
                    res_final = [None,None]
                try:
                    idx = myfile[indices[i[0]]].find('(')
                    res_half = myfile[indices[i[0]]][idx+1:idx+4]
                    res_half = res_half.split(':')
                    res_half = [int(x) for x in res_half]
                except:
                    res_half = [None,None]

                # team names
                idx = myfile[indices[i[0]]-18].find(season + '/') + len(season + '/')
                home_team = myfile[indices[i[0]]-18][idx:]
                idx = home_team.find('/')
                home_team = home_team[0:idx]
                idx = home_team.rfind('-')
                home_team = home_team[0:idx]

                idx = myfile[indices[i[0]]-7].find(season + '/') + len(season + '/')
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
                total_data[i_cont][6] = season
                total_data[i_cont][7] = matchday
                total_data[i_cont][8] = liga_num

                # updating indexs
                i_cont += 1
                sumcum_i += 1

with open(liga + '.csv', 'w') as writeFile:
    writer = csv.writer(writeFile, delimiter=';')
    writer.writerows(total_data)