import glob
import subprocess
import sys

def compare(one, two):
    count = 0
    for l in iter(one.splitlines()):
        # two only contains the line
        # or 
        # two has the line, and lines under it
        # or
        # two has the line at the end, with other lines above
        if l == two or l + "\n" in two or two.endswith("\n" + l):
            count+=1

    #perc = int(count/len(one.splitlines())*100)

    return count


project = "1-2"
if len(sys.argv) > 1:
    project = sys.argv[1]

files = []
if len(sys.argv) > 2:
    files = sorted(sys.argv[2:])
else:
    files = sorted(glob.glob("repo_master_clean_lines/" + project + "/*.txt"))

all_files = sorted(glob.glob("repo_master_clean_lines/" + project + "/*.txt"))

contents = []
all_contents = []

# TODO: Kijk of dit gewoon niet preloaden.
for i, f in enumerate(files):
    s = open(f, "r").read()
    contents.append([f,s])

for i, f in enumerate(all_files):
    s = open(f, "r").read()
    all_contents.append([f,s])

score_matrix = [[-5 for i in range(len(all_files))] for j in range(len(files))]

for i, f in enumerate(contents):
    if len(f[1].splitlines()) == 0:
         #scores = [-2 for x in enumerate(contents)]
         continue

    for j, compare_contents in enumerate(all_contents):
       if f[0] == compare_contents[0]:
           score_matrix[i][j] = -1
           continue

       count = compare(f[1], compare_contents[1])
       score_matrix[i][j] = count

out = ","
for j, f in enumerate(all_files):
    name = f.split("/")
    out += name[-1] + ","
out += ";\n"

for i, row in enumerate(score_matrix):
    name = files[i].split("/")
    out += name[-1] + ","
    for col in row:
        out += str(col) + ","
    out += ";\n"

with open("pythonlog.csv", 'a') as f:
    f.write(out)

print("\n\n\n\nout:")
print(out)
