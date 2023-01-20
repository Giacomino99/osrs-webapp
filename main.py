#! /usr/bin/env python3
''' Creates a Flask server '''
import argparse
from app import app
from sys import stderr

def get_args():
    parser = argparse.ArgumentParser(allow_abbrev = False, description = 'OSRS Calculator Webapp')
    parser.add_argument('port', type = int, help = 'the port at which the server should listen')
    return parser.parse_args()

def main():
    args = get_args()
    port = int(args.port)
    print(f'Attempting to start server on port {port}')
    try:
        app.run(host = '0.0.0.0', port = port, debug = True)
    except Exception as ex:
        print(ex, file = stderr)
        exit(1)

if __name__ == '__main__':
    main()
