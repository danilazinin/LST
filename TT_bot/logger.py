from datetime import datetime as dt


def actions(data):
    time = dt.now().strftime('%H:%M')
    with open('log.csv', 'a') as file:
        file.write('{};entry;{}\n'
                   .format(time, data))