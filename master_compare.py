import gspread
from oauth2client.service_account import ServiceAccountCredentials

from glob import glob
import os
import subprocess
import time

from compare import edit_distance, lines, compare

import xlwt


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
    projects = ["2-1"] #, "2-1", "2-2", "2-3"]

    for project in projects:
        masters = [
            # "https://github.com/timostrating/parkingsimulator",
            # "https://github.com/VincentCremers/Parkeergarage",
            # "https://github.com/rotjeking7/Parkeergarage",
            # "https://github.com/DirkSuelmann2/Parkeergarage",
            # "https://github.com/RamonBonsema08/Parkeergarage",
        ] 
        file = open(project + ".txt")
        for line in file:
            if len(line.strip()) < 10:
                continue
            try:
                dir_name = line.split(" ")[0].replace("\n", "").split(".com/")[1].replace("/", "_")
                open(f"repo_sources/{project}/{dir_name}.txt", "r").read()
                masters.append(line.replace("\n", ""))
            except:
                pass

        for id, line in enumerate(masters):

            dir_name = line.split(" ")[0].replace("\n", "").split(".com/")[1].replace("/", "_")
            print("\n", id, ":", dir_name)
            commits = exc_command(f"cd hanzerepos/{project}/{dir_name} && git rev-list --all --count")
            lines_of_code = exc_command(f"cd repo_sources/{project}/ && cat {dir_name}.txt | wc -l")
            
            update(id+4, 1, line)
            update(1, id+4, line)
            update(id+4, 2, commits)
            update(2, id+4, commits)
            update(id+4, 3, lines_of_code)
            update(3, id+4, lines_of_code)
            
            for id2, line2 in enumerate(masters):
                if id == id2:
                    continue

                dir_name2 = line2.split(" ")[0].replace("\n", "").split(".com/")[1].replace("/", "_")
                value = compare(\
                    open(f"repo_sources/{project}/{dir_name}.txt", "r").read(), 
                    open(f"repo_sources/{project}/{dir_name2}.txt", "r").read())

                if lines_of_code == 0:
                    update(id + 4, id2 + 4, "???")
                else:
                    update(id + 4, id2 + 4, int(float(value) / lines_of_code * 100))
                
                



book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
# client = gspread.authorize(creds)
# worksheet = client.open("data 2.4").worksheet("masters compare")

def update(row, collum, value, wait_time=3): 
    sheet1.write(row, collum, value)

    # if (wait_time > 1000):
    #     wait_time = 1000

    # time.sleep(wait_time)
    # try:
    #     worksheet.update_cell(row, collum, value)
    # except:
    #     print("Trying again in ", wait_time, "seconds")
    #     update(update(row, collum, value, wait_time*2))
        

if __name__ == "__main__":
    main()
    book.save("master_compare_2_1.xls")