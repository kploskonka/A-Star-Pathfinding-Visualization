import configparser
import os

config = configparser.ConfigParser()
if not os.path.exists('../config.ini'):
    config['PARAMETERS'] = {'window_size': '800',
                            'rows': '50'}

    with open('../config.ini', 'w') as configfile:
        config.write(configfile)
else:
    config.read('config.ini')

    try:
        config.get('PARAMETERS', 'window_size')
        config.get('PARAMETERS', 'rows')
    except configparser.NoOptionError:
        print("Config is invalid, please delete config.ini file and generate a new one with proper options")
        exit(-1)

SIZE = int(config.get('PARAMETERS', 'window_size'))
ROWS = int(config.get('PARAMETERS', 'rows'))
GAP = SIZE // ROWS
