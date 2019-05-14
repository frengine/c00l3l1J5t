

from subprocess import call
from os import path

projects = ["1-2", "2-1", "2-2", "2-3"]

call("mkdir hanzerepos", shell=True)

for project in projects:

    file = open(project + ".txt")

    call("mkdir hanzerepos/" + project, shell=True)

    for line in file:
        if len(line.strip()) < 10:
            continue

        url = line.split(" ")[0].replace("\n", "")
        dir_name = url.split(".com/")[1].replace("/", "_")
        print("\n----------")
        print(dir_name)

        if path.isdir("hanzerepos/" + project + "/" + dir_name):
            print("skipping " + dir_name)
            continue

        call("cd hanzerepos/" + project + "/ && git submodule add " + url + " " + dir_name, shell=True)
    
