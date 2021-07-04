import multiprocessing
import os
import hashlib
import array
import numpy as np
import json
import re

def get_one_elf_features(filepath):

    filename = filepath

    # Peframe
    # raw_peframe = os.popen('peframe -j '+filename).read()
    raw_peframe = None
    if raw_peframe:
        tmp_peframe = json.loads(raw_peframe)
        if "ip" in tmp_peframe["strings"]:
            peframe_ip=len(tmp_peframe["strings"]["ip"])
        else:
            peframe_ip=0
        if "url" in tmp_peframe["strings"]:
            peframe_url=len(tmp_peframe["strings"]["url"])
        else:
            peframe_url=0
    else:
        peframe_ip = 0
        peframe_url = 0
    
    # Readelf
    data = os.popen('./mylib/ld-2.27.so ./readelf -h '+filename).read()
    readelf_entry_address=int(data.split("\n")[10].split(":")[1].strip(),16)
    readelf_start_prog_headers=int(re.findall("\d+",data.split("\n")[11].split(":")[1].strip())[0])
    readelf_start_sec_headers=int(re.findall("\d+",data.split("\n")[12].split(":")[1].strip())[0])
    readelf_number_flags=len(data.split("\n")[13].split(":")[1].split(","))
    readelf_header_size=int(re.findall("\d+",data.split("\n")[14].split(":")[1].strip())[0])
    readelf_size_prog_headers=int(re.findall("\d+",data.split("\n")[15].split(":")[1].strip())[0])
    readelf_number_prog_headers=int(re.findall("\d+",data.split("\n")[16].split(":")[1].strip())[0])
    readelf_size_sec_headers=int(re.findall("\d+",data.split("\n")[17].split(":")[1].strip())[0])
    readelf_number_section_headers=int(re.findall("\d+",data.split("\n")[18].split(":")[1].strip())[0])
    readelf_sec_header_string_table_index=int(re.findall("\d+",data.split("\n")[19].split(":")[1].strip())[0])

    # 'strings' command
    data = str(os.popen('strings '+filename).read())
    strings_number=len(data.split("\n"))
    strings_size=len(data)
    strings_avg=float(len(data)/len(data.split("\n")))

    # filesize
    file_size = os.path.getsize(filename)

    # Shannon Entropy  - ent tool
    file_entropy = float(str(os.popen("./mylib/ld-2.27.so ./ent "+filename+" | head -n 1 |  awk '{print $(NF-3)}'").read().strip()))

    # ALL (15 dimension)
    features = [readelf_entry_address, readelf_start_prog_headers, readelf_start_sec_headers, readelf_number_flags, readelf_header_size, readelf_size_prog_headers, readelf_number_prog_headers, readelf_size_sec_headers, readelf_number_section_headers, readelf_sec_header_string_table_index,strings_number,strings_size,strings_avg,file_size,file_entropy]
    features = np.array(features)

    return features

if __name__ == "__main__":
    print(get_one_elf_features("/bin/ls"))

