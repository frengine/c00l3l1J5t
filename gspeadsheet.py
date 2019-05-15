import gspread
from oauth2client.service_account import ServiceAccountCredentials

from glob import glob
import os
import subprocess


def get_to_know_project(project, command):
    dir_name = url.split(".com/")[1].replace("/", "_")
    return safe_check(subprocess.check_output, "cd hanzerepos/"+project+"/"+dir_name+" && " + command, shell=True, universal_newlines=True, encoding='utf-8', errors='ignore')

def safe_check(function, *args, **kwargs):
    try:
        return int(function(*args, **kwargs))
    except Exception:
        return "???"


scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
client = gspread.authorize(creds)
worksheet = client.open("data 2.4").sheet1

projects = ["1-2"] # , "2-1", "2-2", "2-3"]
count= 140

data = { 
    "project": worksheet.range(f'A2:A{count}'), 
    "url": worksheet.range(f'B2:B{count}'),
    "commits": worksheet.range(f'C2:C{count}'),
    "lines of java code": worksheet.range(f'D2:D{count}')
}

for project in projects:

    file = open(project + ".txt")
    id = 0

    for line in file:
        if len(line.strip()) < 10:
            continue

        url = line.split(" ")[0].replace("\n", "")
        print(id, ":", url)

        data["project"][id].value = project
        data["url"][id].value = url
        data["commits"][id].value = get_to_know_project(project, "git rev-list --all --count")
        data["lines of java code"][id].value = get_to_know_project(project, "( find ./ -name '*.java' -print0 | xargs -0 cat ) | wc -l") # TODO add more code extensions
    
        id += 1


for i, row_name in enumerate(data):
    worksheet.update_cell(1, i+1, row_name)
    worksheet.update_cells(data[row_name])