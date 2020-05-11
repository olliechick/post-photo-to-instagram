import os
from file_io import write_to_file


def main():
    print(os.environ)
    username = os.environ['ig_username']
    password = os.environ['ig_password']
    output = '\n'.join([username, password, 'n'])
    write_to_file('in.txt', output)


if __name__ == '__main__':
    main()
