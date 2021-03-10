import os

for folder , sub_folders , files in os.walk(r"C:\Users\customer\CA3\CA3>"):

    print("Currently looking at folder: "+ folder)
    print('\n')
    print("THE SUBFOLDERS ARE: ")
    for sub_fold in sub_folders:
        print("\t Subfolder: "+sub_fold )

    print('\n')

    print("THE FILES ARE: ")
    for f in files:
        print("\t File: "+f)
    print('\n')