import glob
import os

matches_startswith = [
    "package",
    "import",
    "/*",
    "*",
    "//",
    "}",
    "@"
]

matches_equals = [
    "break",
    "continue",
    "else",
]

def keep_essence_of_str(s):
    new_str = ""

    s = s.replace("\t", "").replace(" ", "").replace(";", "").replace("}", "").replace("{", "").replace(":", "")
    lines = s.split("\n")
    for line in lines:
        cont = False
        for m in matches_startswith:
            if line.startswith(m):
                cont = True
                break
        if cont:
            continue

        for m in matches_equals:
            if line == m:
                cont = True
                break
        if cont:
            continue

        if len(line) > 2:
            new_str += line+"\n"

    return new_str

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

files = glob.glob("repo_sources/1-2/*.txt")

#for project in ["1-2", "2-1", "2-2", "2-3"]:
#    mkdir_p("repo_master_clean_lines/" + project)

for i, f in enumerate(files):
    s = keep_essence_of_str(open(f, "r").read())

    with open(f.replace("repo_sources", "repo_master_clean_lines"), 'w') as f:
        f.write(s)
