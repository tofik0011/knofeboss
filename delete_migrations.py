import os
import glob

path_temp = os.path.abspath(__file__)
path = ""
for p in path_temp.split('\\')[:-1]:
    path += f"{p}\\"

dirs = glob.glob(path + "/**/", recursive=True)
dirs_migrations = [d for d in dirs if d.endswith('migrations\\') and not d.__contains__("venv")]

for d in dirs_migrations:
    files_to_delete = [f for f in glob.glob(f"{d}*.py") if not f.__contains__("__init__")]
    for fil in files_to_delete:
        os.remove(fil)
    print(files_to_delete)
