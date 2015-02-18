import sys
import os
import linecache
from random import randrange
import myfunc

pfam_Dir = "../../pfam"
pfamseqdb = "../database/pfamfull/uniref100.pfam27.pfamseq.nr90"

def createHitDB(pfamList, prot_name, work_dir):
    hdl = myfunc.MyDB(pfamseqdb)
    if hdl.failure:
        print "Error"
        return 1
    with open(work_dir + prot_name + ".hits.db.temp", "w") as outFile:
        for pfamid in pfamList:
            record = hdl.GetRecord(pfamid)
            if record:
                outFile.write(record)
        hdl.close()

    os.system("python my_uniqueseq.py " + work_dir + prot_name + ".hits.db.temp")


def main(argvs):
    input_file = argvs[1]
    work_dir = argvs[2]

    name_temp = (input_file[input_file.rfind("/")+1:])
    name = name_temp[:name_temp.rfind(".")]
    startDir = os.getcwd()
    os.chdir(os.path.abspath("../database/pfam_seq/PfamScan/"))
    sCmd = "perl " + "pfam_scan.pl" + " -fasta " + input_file + " -dir " + pfam_Dir + " -outfile " + work_dir + name + ".txt"
    os.system(sCmd)
    os.chdir(startDir)

    pfamList = []
    pattern = "# <seq id> <alignment start> <alignment end> <envelope start> <envelope end> <hmm acc> <hmm name> <type> <hmm start> <hmm end> <hmm length> <bit score> <E-value> <significance> <clan>"
    bFoundStart = False
    with open(work_dir + name + ".txt") as inFile:
        for line in inFile:
            if line.find(pattern) != -1:
                bFoundStart = True
            if bFoundStart is True:
                pos = line.find("PF")
                if pos != -1:
                    pfamList.append(line[pos:pos+7])

    createHitDB(list(set(pfamList)), name, work_dir)

if __name__ == "__main__":
    main(sys.argv)