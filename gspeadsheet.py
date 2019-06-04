import gspread
from oauth2client.service_account import ServiceAccountCredentials

from glob import glob
import os
import subprocess

from compare import edit_distance, lines

TO_MUCH_CODE_THRESHHOLD = 7500


def exc_command(command):
    return safe_check(subprocess.check_output, command, shell=True, universal_newlines=True, encoding='utf-8', errors='ignore')

def safe_check(function, *args, **kwargs):
    try:
        return int(function(*args, **kwargs))
    except Exception:
        return "???"

def at_most_x_lines_in_common(project, myrepo_url):
    try:
        myrepo_string = open(myrepo_url, "r").read()

        maximum = 0
        for repo_file_url in glob(f"repo_sources/{project}/*"):
            if(repo_file_url == myrepo_url or exc_command(f"cat {repo_file_url} | wc -l") > TO_MUCH_CODE_THRESHHOLD):
                continue
            maximum = max(maximum, lines(myrepo_string, open(repo_file_url, "r").read()))
            print(".", end="")

        return maximum

    except:
        return "???"

def main():
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    worksheet = client.open("data 2.4").sheet1

    projects = ["1-2"] #, "2-1", "2-2", "2-3"]
    count= 250

    data = { 
        "project": worksheet.range(f'A3:A{count}'), 
        "url": worksheet.range(f'B3:B{count}'),
        "commits": worksheet.range(f'C3:C{count}'),
        "commits met 10+ regels": worksheet.range(f'D3:D{count}'),
        "lines of code": worksheet.range(f'E3:E{count}'),
        "clean lines of code": worksheet.range(f'F3:F{count}'),
        "file count": worksheet.range(f'G3:G{count}'),
    }

    id = 0
    for project in projects:

        file = open(project + ".txt")

        for line in file:
            if len(line.strip()) < 10:
                continue

            url = line.split(" ")[0].replace("\n", "")
            dir_name = url.split(".com/")[1].replace("/", "_")
            print("\n", id, ":", url)

            data["project"][id].value = project
            data["url"][id].value = url
            data["commits"][id].value = exc_command(f"cd hanzerepos/{project}/{dir_name} && git rev-list --all --count")
            data["commits met 10+ regels"][id].value = "ToDo"
            data["lines of code"][id].value = exc_command(f"cd repo_sources/{project}/ && cat {dir_name}.txt | wc -l")
            data["clean lines of code"][id].value = "ToDo"
            data["file count"][id].value = exc_command(f"find hanzerepos/{project}/{dir_name} -type f | wc -l")
            id += 1


    for i, row_name in enumerate(data):
        worksheet.update_cell(1, i+1, row_name)
        worksheet.update_cells(data[row_name])


if __name__ == "__main__":
    main()