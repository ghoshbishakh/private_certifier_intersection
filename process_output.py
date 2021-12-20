import sys

fname = sys.argv[1]

with open(fname, "r") as f:
    alllines = f.readlines()

    timeline = alllines[-3].strip()
    dataline = alllines[-2].strip()
    global_dataline = alllines[-1].strip()

    x = ", ".join([timeline.split(" ")[2], dataline.split(" ")[3],  dataline.split(" ")[4], global_dataline.split(" ")[4], global_dataline.split(" ")[5]])
    print(x)