import re
from geopy import geocoders

HEADERS = ['Ind', 'Name', 'Latitude', 'Longitude', 'Elevation', 'Judet', 'Regiune']
REGIUNI = {'Cluj': ['CJ', 'BN', 'MS'],
           'Vest': ['TM', 'AR', 'BH'],
           'Baia Mare': ['MM', 'SM', 'SJ'],
           'Centru': ['HD', 'AB', 'SB'],
           'Brasov': ['BV', 'CV', 'HR'],
           'Moldova Nord': ['SV', 'BT', 'NT', 'IS'],
           'Moldova Sud': ['BC', 'VS', 'VN'],
           'Baragan': ['GL', 'TL', 'BZ', 'BR'],
           'Dobrogea': ['CT', 'CL', 'IL'],
           'Bucuresti': ['B', 'IF', 'GR', 'TR'],
           'Muntenia': ['PH', 'AG', 'DB'],
           'Sud': ['GJ', 'VL'],
           'Oltenia': ['OT', 'MH', 'DJ', 'CS']
}

REGIUNI_IST = {'Transilvania': ['CJ', 'BN', 'MS', 'HD', 'AB', 'SB', 'BV', 'CV', 'HR', 'SJ'],
           'Banat': ['TM', 'CS'],
           'Crisana': ['BH', 'AR'],
           'Maramures': ['MM', 'SM', ],
           'Bucovina': ['SV', 'BT'],
           'Moldova': ['BC', 'VS', 'VN', 'NT', 'IS', 'GL'],
           'Muntenia': ['PH', 'AG', 'DB', 'B', 'IF', 'GR', 'TR', 'IL', 'BZ', 'BR', 'CL',],
           'Dobrogea': ['CT',  'TL'],
           'Oltenia': ['OT', 'MH', 'DJ', 'GJ', 'VL']
}

UNK = {"BOBOC AIR BASE": "BOBOC, BZ",
        "BORCEA FETESTI AIR BASE": "FETESTI",
        "SIGHETUL MARMATIEI": "SIGHETU MARMATIEI",
        "BAIA MARE/MAGHERUSI": "BAIA MARE",
        "CIMPULUNG MOLDOVENE": "CIMPULUNG MOLDOVENESC",
        "CLUJ-NAPOCA/SOMESEN": "CLUJ-NAPOCA",
        "TIGU MURES/VIDRASA": "TARGU MURES",
        "SFANTU GHEORGHE GOVASNA": "SFANTU GHEORGHE, CV",
        "GORGOVA": "GORGOVA, TL",
        "FAUREI/=694514 KQYB": "FAUREI",
        "SFANTU GHEORGHE DELTA": "SFANTU GHEORGHE, TL",
        "GURA PORTITEI": "GURA PORTITEI, TL",
        "SARBATO": "SARBATOAREA",
        "GREACA": "GREACA, GR",
}

stations = []

def get_region(county):
    for cnt in REGIUNI_IST.keys():
        if county in REGIUNI_IST[cnt]:
            return cnt
    
    return 'None'

geo = geocoders.GeoNames(username='cristi.domsa')

with open('/media/cristi/DATA/projects/inflectionPoint/weather/stations.txt', 'r') as f:
    text = f.read()

    pattern =  r"^(\d+)\s+\d+\s+(.+)\s+ROMANIA\s+([+]\S+)\s+([+]\S+)\s+([+]\S+)\s*$"

    matches = re.finditer(pattern, text, re.MULTILINE)

    for matchNum, match in enumerate(matches):        
        
        matchNum = matchNum + 1
        station = []
    
        #print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
    
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            
            station.append(match.group(groupNum).strip())
            #print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
        if float(station[4]) < 1000.0:
            try:
                info = geo.geocode(station[1] + ', Romania')
                if info == None:
                    info = geo.geocode(UNK[station[1]] + ', Romania')
                county = info.raw['adminCodes1']['ISO3166_2']
                station.append(county)
                station.append(get_region(county))
                stations.append(station)

            except Exception as e:
                print('location - {} - Error!'.format(station[1]))

            

with open('/media/cristi/DATA/projects/inflectionPoint/geo/stations_8.csv', 'w') as f:
    f.write(','.join(HEADERS) + '\n')
    for s in stations:
        f.write(','.join(s) + '\n')