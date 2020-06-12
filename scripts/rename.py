import os

DIR_TO_CHECK = 'files to check'

files = os.listdir(DIR_TO_CHECK)

for i in range(len(files)):
    path = DIR_TO_CHECK + '/' + files[i]
    new_name = DIR_TO_CHECK + '/' + 'fl stock (' + str(i) + ').wav'
    os.rename(path, new_name)
