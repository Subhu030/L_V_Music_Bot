from os import listdir

bgs = []
for file in listdir("RiruruMusic/assets"):
    if file.endswith("png"):
        bgs.append(file[:-4])
