import os

def get_path(file_path):
    projetc_path = os.getcwd().split(os.sep)
    path_array = file_path.split('/')
    path = projetc_path + path_array

    return os.sep.join(str(x) for x in path)


