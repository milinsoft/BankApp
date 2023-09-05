from os.path import exists


def get_file_path() -> str:
    file_path = False
    while not file_path:
        file_path = input('Please provide the path to your file: ').strip("'\"")
        if not exists(file_path):
            print('Incorrect file path, please try again!')
            file_path = False
    return file_path
