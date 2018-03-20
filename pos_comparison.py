
# coding : utf-8
# author : Marianne Reboul
# This software generates a csv with statistics on POStags on a tagged corpus (with the Alix software)


import os
import fnmatch
from lxml import etree
from collections import OrderedDict
import csv
import argparse


print('This software generates a csv with statistics on POStags on a selected corpus \nusage: --dir path/to/your/source/dir --csv path/to/your/target/directory/for/csv')
parser = argparse.ArgumentParser()
parser.add_argument('--dir', help= '/your/directory/to/tagged/files/')
parser.add_argument('--csv', help= '/your/directory/to/your/csv/file/')
args = parser.parse_args()


path_to_folder=args.dir
files_list=fnmatch.filter(os.listdir(path_to_folder), '*.xml')


dic_stats_first=OrderedDict()
dic_stats_last=OrderedDict()


def stats_POS (elem, pos, entry, map_stats):
    nb_pos = len(elem.findall(".//word[@postag='"+pos+"']"))
    if entry in map_stats.keys():
        prev_val = map_stats[entry]
        map_stats[entry] = prev_val+nb_pos
    else :
        map_stats[entry] = nb_pos
    
    return map_stats


for file in files_list:
    tmpFile=file.replace("/",":")
    full_path=path_to_folder+tmpFile
    if os.path.isfile(full_path):
        tree=etree.parse(full_path)
        if tree.findall(".//div[@type='chapter']"):
            elem_first = tree.findall(".//div[@type='chapter']")[0]
            dic_stats_first = stats_POS(elem_first, 'NAME', "name_first", dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'NAMEpersf', 'name_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'NAMEpersm', 'name_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'NAMEplace', 'name_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'NAMEgod', 'name_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'VERB', 'verb_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'CONJsubord', 'sub_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'CONJcoord', 'coord_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'PUNcl', 'light_pun_first', dic_stats_first)
            dic_stats_first = stats_POS(elem_first, 'PUNsent', 'sent_pun_first', dic_stats_first)

            elem_last = tree.findall(".//div[@type='chapter']")[len(tree.findall(".//div[@type='chapter']"))-1]
            dic_stats_last = stats_POS(elem_last, 'NAME', 'name_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'NAMEpersf', 'name_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'NAMEpersm', 'name_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'NAMEplace', 'name_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'NAMEgod', 'name_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'VERB', 'verb_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'CONJsubord', 'sub_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'CONJcoord', 'coord_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'PUNcl', 'light_pun_last', dic_stats_last)
            dic_stats_last = stats_POS(elem_last, 'PUNsent', 'sent_pun_last', dic_stats_last)
                
    print('File done : '+file)


with open(args.csv+'pos_analysis.csv', 'a') as f:
    headers=list()
    merged=dict()
    
    for (k,v), (k2,v2) in zip(dic_stats_first.items(), dic_stats_last.items()):
        headers.append(k)
        headers.append(k2)
        merged[k]=v
        merged[k2]=v2
        
    writer = csv.DictWriter(f, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    writer.writerow(merged)

