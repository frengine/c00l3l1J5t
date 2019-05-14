from glob import glob
import os
import subprocess

extentions = ["bat", "bluej", "c", "cpp", "css", "d", "frag", "glsl", "gradle", "h", "html", "ino", "java", "js", "php", "phpt", "py", "scss", "sh", "sql", "ts", "vert"]

projects = ["1-2", "2-1", "2-2", "2-3"]
os.makedirs("repo_commits", exist_ok=True)

for project in projects:

    prj_dir = "hanzerepos/" + project
    os.makedirs("repo_commits/" + project, exist_ok=True)

    for repo_dir in glob(prj_dir + "/*/"):
        log = os.popen("cd " + repo_dir + " && git --no-pager log --no-color").read()
        commits = []

        os.makedirs(repo_dir.replace("hanzerepos", "repo_commits"), exist_ok=True)

        for line in [line for line in log.split("\n") if line.startswith("commit")]:
            commits.append(line.split(" ")[1])

        i = 0
        for commit in commits:
            
            commit_txt = ""

            diff = subprocess.check_output("cd " + repo_dir + " && git --no-pager show --no-color " + commit, shell=True, universal_newlines=True, encoding='utf-8', errors='ignore')

            valid_file = False
            for line in diff.split("\n"):
                if line.startswith("+++ "):
                    valid_file = False
                    for ext in extentions:
                        if line.endswith("." + ext):
                            valid_file = True
                            break
                    continue

                if not valid_file:
                    continue
                if line.startswith("+"):
                    commit_txt += line[1:] + "\n"
            
            print("\n\n---------------------\n" + commit_txt)

            if len(commit_txt) == 0:
                continue
                
            dst = open(repo_dir.replace("hanzerepos", "repo_commits") + str(i) + "_" + commit + ".txt", "w")
            dst.write(commit_txt)
            dst.close()
            i += 1
                



