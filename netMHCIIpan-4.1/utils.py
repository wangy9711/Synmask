from collections import defaultdict
import csv
import os
import pathlib
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_recall_fscore_support
import pandas as pd
import numpy as np

# ./netMHCIIpan -f ./mydata/test1.pep -inptype 1 -a DRB1_0101

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
            f.writelines(f"./netMHCIIpan -f {os.path.join(input_folder_path, file)} -xls -inptype 1 -a {pathlib.Path(file).stem} -xlsfile {os.path.join(output_folder_path, pathlib.Path(file).stem +'.xls')}\n")


def mergedata_NetMHC(data_path, output_csvfile):
    hla_files = os.listdir(data_path)

    with open(output_csvfile, "w") as f1:
        w = csv.writer(f1)
        w.writerow(["peptide", "HLA", "NB"])

        for hla_file in hla_files:
            with open(os.path.join(data_path, hla_file), "r") as f2:
                r = csv.reader(f2, delimiter='\t')
                hla = next(r)[4]
                next(r)
                for line in r:
                    w.writerow([line[1], hla, line[8].strip()])


def statistic(predict_csvfile, y_csvfile):
    df = pd.read_csv(predict_csvfile)
    predicts_test = np.array(df["NB"].to_list())
    
    pep_hla = df["peptide"] + '-' + df["HLA"]

    y_dict = {}
    with open(y_csvfile, "r") as f:
        r = csv.reader(f)
        next(r)
        for line in r:
            y_dict[line[0]+"-"+line[1]] = int(line[2])
    y_test = []
    for p_h in pep_hla:
        y_test.append(y_dict[p_h])
    
    y_test = np.array(y_test)

    tn, fp, fn, tp = confusion_matrix(y_test, predicts_test).ravel()
    sensitive = tp / (tp + fn)
    specificity = tn / (tn+fp)
    print(f"sensitive: {sensitive}")
    print(f"specificity: {specificity}")
    p, r, f, _ = precision_recall_fscore_support(y_test, predicts_test, pos_label=1, average="macro")
    print("p: {},r: {},f: {}".format(p, r, f))
    print("acc: {}".format(accuracy_score(y_test,predicts_test)))

test_file = "/mnt/data/dengyifan/immuno/II/modified_data/total/benchmark/total1_test"
input_folder_path = "/mnt/data/dengyifan/immuno/II/modified_data/total/temp/input"
# convert_format(test_file, input_folder_path)

output_folder_path = "/mnt/data/dengyifan/immuno/II/modified_data/total/temp/output/"
bashfile = "/home/dengyifan/gitlab/ImmunoPredictTool/NetMHCpan/netMHCIIpan-4.1/predict_bench.sh"
# generate_bash(input_folder_path, output_folder_path, bashfile)


output_csvfile = "/mnt/data/dengyifan/immuno/II/modified_data/total/temp/output.csv"
# mergedata_NetMHC(output_folder_path, output_csvfile)

y_csvfile = "/mnt/data/dengyifan/immuno/II/modified_data/total/benchmark/total1_test"
# y_csvfile = "/home/dengyifan/gitlab/ImmunoPredictTool/data-zl/MCH-II/netMHCIIpan_output.txt"

# statistic(output_csvfile, y_csvfile)