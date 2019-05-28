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
    worksheet = client.open("data 2.4").worksheet("masters compare")

    projects = ["1-2"] #, "2-1", "2-2", "2-3"]

    data = worksheet.range(f'B2:F6')

    for project in projects:
        masters = [
            "https://github.com/timostrating/parkingsimulator",
            "https://github.com/VincentCremers/Parkeergarage",
            "https://github.com/rotjeking7/Parkeergarage",
            "https://github.com/DirkSuelmann2/Parkeergarage",
            "https://github.com/RamonBonsema08/Parkeergarage",
        ] # open(project + ".txt")
        # if len(line.strip()) < 10:
        #     continue

        for id, line in enumerate(masters):
            for id2, line2 in enumerate(masters):
                if id == id2:
                    continue

                url = line.split(" ")[0].replace("\n", "")
                dir_name = url.split(".com/")[1].replace("/", "_")
                print("\n", id * len(masters) + id2, ":", url)

                data[id * len(masters) + id2].value = id * len(masters) + id2

    #         data["project"][id].value = project
    #         data["url"][id].value = url
    #         data["commits"][id].value = exc_command(f"cd hanzerepos/{project}/{dir_name} && git rev-list --all --count")
    #         data["commits met 10+ regels"][id].value = "ToDo"
    #         data["lines of code"][id].value = exc_command(f"cd repo_sources/{project}/ && cat {dir_name}.txt | wc -l")
    #         data["clean lines of code"][id].value = "ToDo"
    #         data["file count"][id].value = exc_command(f"find hanzerepos/{project}/{dir_name} -type f | wc -l")


        worksheet.update_cells(data)


if __name__ == "__main__":
    main()