with open("examlist.txt", "r") as infile, open("examlist2.txt", "w") as outfile:
    for line in infile:
        line = line.strip()
        if not line:
            continue  # Skip blank lines
        words = line.split()
        csv_line = ",".join(words)
        outfile.write(csv_line + "\n")