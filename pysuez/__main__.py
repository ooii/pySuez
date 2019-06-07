import argparse
import sys
import json

from pysuez import SuezClient


def main():
    """Main function"""
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--username',
                        required=True, help='Suez username')
    parser.add_argument('-p', '--password',
                        required=True, help='Password')
    parser.add_argument('-c', '--counter_id',
                        required=True, help='Counter Id')

    args = parser.parse_args()

    client = SuezClient(args.username, args.password, args.counter_id)

    try:
    	client.update()
    except BaseException as exp:
        print(exp)
        return 1
    finally:
        client.close_session()
    print (client.attributes)

if __name__ == '__main__':
    sys.exit(main())