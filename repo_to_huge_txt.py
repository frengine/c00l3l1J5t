
from glob import glob
import os
import fnmatch
import re

extentions = ["bat", "bluej", "c", "cpp", "css", "d", "frag", "glsl", "gradle", "h", "html", "ino", "java", "js", "php", "phpt", "py", "scss", "sh", "sql", "ts", "vert"]
includes = '|'.join([fnmatch.translate("*." + x) for x in extentions])

projects = ["1-2", "2-1", "2-2", "2-3"]
os.makedirs("repo_sources", exist_ok=True)

for project in projects:

    prj_dir = "hanzerepos/" + project
    os.makedirs("repo_sources/" + project, exist_ok=True)

    for repo_dir in glob(prj_dir + "/*/"):
        print("\n\n-------\n", repo_dir)

        src_files = []
        src_txt = ""

        for root, dirs, files in os.walk(repo_dir):
            src_files.extend(
                [
                    (root if root.endswith("/") else root + "/") 
                        + f 
                    
                    for f in files 
                    if re.match(includes, f)
                ]
            )

        for f in src_files:
            opened = open(f, "rb")
            src = opened.read().decode(errors="replace")
            src_txt += src

        dst = open(repo_dir.replace("hanzerepos", "repo_sources")[:-1] + ".txt", "w")
        dst.write(src_txt)
        dst.close()




