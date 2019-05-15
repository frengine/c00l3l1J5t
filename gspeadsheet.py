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
        "project": worksheet.range(f'A2:A{count}'), 
        "url": worksheet.range(f'B2:B{count}'),
        "commits": worksheet.range(f'C2:C{count}'),
        "lines of code": worksheet.range(f'D2:D{count}'),
        "file count": worksheet.range(f'E2:E{count}'),
        "aantal regels exact in andere repo te vinden": worksheet.range(f'F2:F{count}')
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
            count = exc_command(f"cd repo_sources/{project}/ && cat {dir_name}.txt | wc -l")
            data["lines of code"][id].value = count
            data["file count"][id].value = exc_command(f"find hanzerepos/{project}/{dir_name} -type f | wc -l")
            if count < TO_MUCH_CODE_THRESHHOLD:
                data["aantal regels exact in andere repo te vinden"][id].value = at_most_x_lines_in_common(project, f"repo_sources/{project}/{dir_name}.txt")
            else:
                data["aantal regels exact in andere repo te vinden"][id].value = "included other data"
            id += 1


    for i, row_name in enumerate(data):
        worksheet.update_cell(1, i+1, row_name)
        worksheet.update_cells(data[row_name])


if __name__ == "__main__":
    main()