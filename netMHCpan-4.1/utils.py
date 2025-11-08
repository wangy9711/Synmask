from collections import defaultdict
import csv
import os
import pathlib
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd
import numpy as np
import re

def convert_format(test_file, folder_path):
    contents = defaultdict(list)
    with open(test_file, "r") as f:
        r = csv.reader(f)
        next(r)
        for line in r:
            contents[line[1]].append(line[0])

    for hla, values in contents.items():
        with open(os.path.join(folder_path,hla+".txt"), "w") as f:
            for v in values:
                f.writelines(v+"\n")

def generate_bash(input_folder_path, output_folder_path, bashfile):
    files = os.listdir(input_folder_path)
    with open(bashfile, "w") as f:
        for file in files:
            f.writelines(f"./netMHCpan -p {os.path.join(input_folder_path, file)} -xls -a {pathlib.Path(file).stem} -xlsfile {os.path.join(output_folder_path, pathlib.Path(file).stem +'.xls')} -l 8,9,10,11,12,13,14,15\n")


def mergedata_NetMHC(data_path, output_csvfile):
    hla_files = os.listdir(data_path)

    with open(output_csvfile, "w") as f1:
        w = csv.writer(f1)
        w.writerow(["peptide", "HLA", "NB"])

        for hla_file in hla_files:
            with open(os.path.join(data_path, hla_file), "r") as f2:
                r = csv.reader(f2, delimiter='\t')
                hla = next(r)[3]
                next(r)
                for line in r:
                    w.writerow([line[1], hla, line[8].strip()])


def statistic(predict_csvfile, y_csvfile):
    # 当有非标准氨基酸或者奇怪的字母？？出现的时候，预测结果会将其更改成X

    df = pd.read_csv(predict_csvfile)
    predicts_test = np.array(df["NB"].to_list())
    
    pep_hla = df["peptide"] + '-' + df["HLA"]

    y_dict = {}
    with open(y_csvfile, "r") as f:
        r = csv.reader(f)
        next(r)
        for line in r:
            seq = re.sub("[^ALIVPFMWGSQTCNYDEKRH]","X",line[0])
            y_dict[seq+"-"+line[1]] = int(line[2])
    y_test = []
    for p_h in pep_hla:
        y_test.append(y_dict[p_h])
    
    y_test = np.array(y_test)
    print(y_test)

    tn, fp, fn, tp = confusion_matrix(y_test, predicts_test).ravel()
    sensitive = tp / (tp + fn)
    specificity = tn / (tn+fp)
    print(f"sensitive: {sensitive}")
    print(f"specificity: {specificity}")
    p, r, f, _ = precision_recall_fscore_support(y_test, predicts_test, pos_label=1, average="macro")
    print("p: {},r: {},f: {}".format(p, r, f))
    print("acc: {}".format(accuracy_score(y_test,predicts_test)))


test_file = "/mnt/data/dengyifan/immuno/I/modified_data/tcell/all_tcell"
input_folder_path = "/mnt/data/dengyifan/immuno/I/netmhc/train/NetMHCpan_train/tmp/input"
convert_format(test_file, input_folder_path)

output_folder_path = "/mnt/data/dengyifan/immuno/I/netmhc/train/NetMHCpan_train/tmp/output"
bashfile = "/home/dengyifan/gitlab/ImmunoPredictTool/NetMHCpan/netMHCpan-4.1/predict_tcell.sh"
generate_bash(input_folder_path, output_folder_path, bashfile)

output_csvfile = "/mnt/data/dengyifan/immuno/I/netmhc/train/NetMHCpan_train/tmp/predict_netmhc_tcell.csv"
# mergedata_NetMHC(output_folder_path, output_csvfile)

# statistic(output_csvfile, test_file)



# output_csvfile = "/mnt/data/dengyifan/immuno/II/modified_data/total/temp/output.csv"
# test_file = "/mnt/data/dengyifan/immuno/II/modified_data/total/benchmark/total1_test"

# df1 = pd.read_csv(output_csvfile)
# pep_hla1 = df1["peptide"] + '__' + df1["HLA"]
# B = pep_hla1.to_list()

# df2 = pd.read_csv(test_file)
# pep_hla2 = df2["Peptide"] + '__' + df2["MHC"]
# A = pep_hla2.to_list()
# A = []
# for p_h in pep_hla2.to_list():
#     pep, hla = p_h.split("__")
    # seq = re.sub("[^ALIVPFMWGSQTCNYDEKRH]","X",pep)
    # A.append(seq+"__"+hla)

# out = set()
# for i in list(set(A) - set(B)):
    # out.add(i.split("__")[1].split("-")[0])

# print(list(set(A) - set(B)))