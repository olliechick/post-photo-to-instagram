import os
from file_io import write_to_file


def main():
    username = os.environ['ig_username']
    password = os.environ['ig_password']
    output = '\n'.join([username, password, 'n', '1'])
    write_to_file('in.txt', output)


if __name__ == '__main__':
    main()
