import os, sys, subprocess, shutil, argparse, json

pg_list=["Gaussian", "ADF", "Orca"]

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


parser=MyParser()
parser.add_argument( '--program', dest='prog', type=str, help='Define for which program the input is needed', default="")
parser.add_argument( '--list', dest='list', help='list all implemented softwares', action='store_true')
parser.add_argument( '--setup', dest='setup', type=str, help='initialize guided setup', default="")
parser.add_argument( '--calc', dest='calc', type=str, help='calculation type', default="opt")
parser.add_argument( '--bas', dest='bas', type=str, help='basis set type', default="6-31G")
parser.add_argument( '--funct', dest='funct', type=str, help='functional type', default="BLYP")
parser.add_argument( '--chg', dest='charge', type=int, help='molecule charge', default="0")
parser.add_argument( '--spin', dest='spin', type=int, help='spin multiplicity', default="0")
parser.add_argument( '--title', dest='title', type=str, help='job name', default="MOLECULE")
parser.add_argument( '--crd', dest='crd', type=str, help='coordinates file', default="")
parser.add_argument( '--ncpu', dest='ncpu', type=str, help='number of cores used for the calculation', default="4")
parser.add_argument( '--mem', dest='mem', type=str, help='RAM used for the calculation', default="16GB")
parser.add_argument( '--add', dest='add_input', type=str, help='Additional input to be written.\n Should appear exactly as in input file.\n Each newline separated by .', default="")
args = parser.parse_args()





if args.setup != "":
    calc_typ=input("Calculation type \n 1 Optimization \n" +
        " 2 Optimization + Frequencies \n 3 Transition State \n 4 Other \n" )
    if calc_typ == "4":
        cust_par=input("Custom input line: ")
        chg=input("Total Charge: ")
        mult=input("Spin Multiplicity: ")
    else:
        bas=input("Basis Set:" )
        funct=input("Density Functional: " )
        chg=input("Total Charge: ")
        mult=input("Spin Multiplicity: ")



head=open("head", "w")
coords=open(args.crd, "r")
crd_lines=coords.readlines()
lines=[]
###############Gaussian##################################
if args.prog == "Gaussian":
    lines.append("%Nprocs=24\n%Chk=" + args.title + "\n%Mem=16000MB\n")
    lines.append("#p " + args.calc + " " + args.funct + "/" + args.bas + "\n\n")
    lines.append(args.title + "\n\n")
    lines.append(str(args.charge) + " " + str(args.spin) + "\n")
    for line in crd_lines:
        lines.append(line)
###########ADF#############################################
elif args.prog == "ADF":
    ADF_dict=json.load(open('ADF.json','r'))
    lines.append("ATOMS\n")
    for line in crd_lines:
        lines.append(line)
    lines.append("END\n\n")

    #symmetry and Charge
    lines.append("SYMMETRY " + ADF_dict["symmetry"])
    lines.appedn("CHARGE " + ADF_dict["charge"] + " " + ADF_dict["multiplicity"])

    #geometry
    lines.append("GEOMETRY\n")
    lines.append("ITERATIONS " + ADF_dict["iterations"])
    lines.append("CONVERGE " + ADF_dict["converge"])
    lines.append("END\n\n")
    #scf
    lines.append("SCF\n")
    lines.append("ITERATIONS " + ADF_dict["iterations"])
    lines.append("CONVERGE " + ADF_dict["scf_converge"])
    lines.append("END\n\n")
    #other
    lines.append("NUMERICALQUALITY " + ADF_dict["quality"])
    lines.append(ADF_dict["relativistic"])
    lines.append(args.add_input.replace('.','\n'))
    lines.append(add_input.replace('.','\n'))
    #END
    lines.append("END INPUT")





for i in lines:
    head.write(i)

'''
    head=open("head", "r")
    head_procsd=open("htemp","w")
    hlines=head.readlines()

    if calc_typ=="4":
        hlines.append("\n#p "+ cust_par)
        hlines.append("\n\n" + args.title)
        hlines.append("\n\n" + chg + " " + mult)
        for item in hlines:
         head_procsd.write("%s" % item)
    else:
        if calc_typ=="1":
            typ="opt "
        elif calc_typ=="2":
            typ="opt freq "
        elif calc_typ=="3":
            typ="opt(TS,noeigen,calcFC) "

        hlines.append("\n#p " + typ + funct + "/" + bas)
        hlines.append("\n\n" + args.title)
        hlines.append("\n\n" + chg + " " + mult)
        for item in hlines:
            head_procsd.write("%s" % item)
'''

if args.list:
    print("Currently available softwares: Gaussian, ADF, Orca")
    sys.exit()

if args.prog not in pg_list:
    print("No valid software provided. To see a list of all the implemented softwares use the --list argument")
