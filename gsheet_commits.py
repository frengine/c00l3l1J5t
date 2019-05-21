from compare import edit_distance
files = [
    "repo_commits/1-2/360456_parkeer1/0_5d97a22efa44fa79f060fe2df00665433eea55f8.txt",
    "repo_commits/1-2/360456_Testerd/0_b5ea847045222730e592ff2cb41320d104cf1057.txt",
    "repo_commits/1-2/360456_Testerd/10_39c299b3aa82b0f9fddc26a4d13f9970d0947970.txt",
    "repo_commits/1-2/Afrobee1_Project-Parkeergarage/0_b77d267d035b5dd16c42b83a1512b96d12b1b38e.txt"
]

def keep_essence_of_str(s):
    new_str = ""
    s = s.replace("\t", "").replace(" ", "")
    lines = s.split("\n")
    for line in lines:
        if line.startswith("package") or line.startswith("import") or line.startswith("/*") or line.startswith("*") or line.startswith("//") or line.startswith("}"):
            continue

        if(len(line) > 2):
            new_str += line

    print(new_str)
    return s

score_matrixs = [ 
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]

for i, file in enumerate(files):
    s = keep_essence_of_str(open(file, "r").read())
    
    for j, compare_file in enumerate(files):
        score = edit_distance(s, keep_essence_of_str(open(compare_file, "r").read()))
        print(score)
        score_matrixs[i][j] = score


for row in score_matrixs:
    print(row)