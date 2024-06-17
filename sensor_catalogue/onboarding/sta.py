import frost_sta_client as sta
import secd_staplus_client as staplus
from geojson import Point
from frost_sta_client.service.auth_handler import AuthHandler

# url = "https://score.sta.tero.gr/v1.0"
url = "https://score.tst.tero.gr/v1.1"

auth = AuthHandler(username="write", password="write")
service = staplus.STAplusService(url, auth_handler=auth)
print(service)

thing = staplus.Thing(
    'SCORE - Jaizkibel Station test 1',
    'This station is named Jaizkibel, same name of the '
    'mountain where is located',
    properties={'CCLL': 'Oarsoaldea'},
    locations=[staplus.Location(
        name='Jaizkibel Station',
        description='Gipuzkoa Province, Lezo Municipality',
        location=Point((-1.85972, 43.3446)),
        encoding_type='application/geo+json',
        properties={'CCLL': 'Oarsoaldea'}
    )]
)

service.create(thing)
print(thing)
