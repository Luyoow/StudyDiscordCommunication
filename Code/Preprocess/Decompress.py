import zipfile
import os

root = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../..")) # get ccurrent dir
data_root = root + "/Data/DataZIP/"   # input：location
zip_root = root + "/Data/DataJSON/"   # output：location

#print(data_root)
dirs = os.listdir(data_root)
for per_zip in dirs:
    print(per_zip)
    zip_dir = data_root + per_zip
    f = zipfile.ZipFile(zip_dir,'r')  # zipfile: location
    for file in f.namelist():
        f.extract(file, zip_root + per_zip.split('.')[0] + "/")               # Decompress: location
    f.close()