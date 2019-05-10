import os, sys, subprocess, shutil, argparse, json

pg_list=["Gaussian", "ADF", "Orca"]

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)
lines=[]

parser=MyParser()
parser.add_argument( '--program', dest='prog', type=str, help='Define for which program the input is needed', default="")
parser.add_argument( '--list', dest='list', help='list all implemented softwares', action='store_true')
parser.add_argument( '--setup', dest='setup', help='initialize guided setup', action='store_true')
parser.add_argument( '--calc', dest='calc', type=str, help='calculation type', default="")
parser.add_argument( '--bas', dest='bas', type=str, help='basis set type', default="")
parser.add_argument( '--funct', dest='funct', type=str, help='functional type', default="")
parser.add_argument( '--chg', dest='charge', type=str, help='molecule charge', default="")
parser.add_argument( '--spin', dest='spin', type=str, help='spin multiplicity', default="")
parser.add_argument( '--title', dest='title', type=str, help='job name', default="")
parser.add_argument( '--crd', dest='crd', type=str, help='coordinates file', default="")
parser.add_argument( '--ncpu', dest='ncpu', type=str, help='number of cores used for the calculation', default="")
parser.add_argument( '--mem', dest='mem', type=str, help='RAM used for the calculation', default="")
parser.add_argument( '--add', dest='add_input', type=str, help='Additional input to be written.\n Should appear exactly as in input file.\n Each newline separated by .', default="")
args = parser.parse_args()

def ADF_opt(type, iterations, converge):
    type=args.opt
    iterations=dict["iterations"]
    converge=dict["converge"]





gendict=json.load(open('gendict.json', 'r'))

add_input=""
if args.prog=="Gaussian":
    dict=json.load(open('Gaussian.json', 'r'))
elif args.prog=="ADF":
    dict=json.load(open('ADF.json', 'r'))
elif args.prog=="ORCA":
    dict=json.load(open('ORCA.json', 'r'))

if args.calc = "opt":
    if args.prog=="Gaussian":
        dict["opt"]="opt"
    elif args.prog=="ADF":
        dict["opt"]=""
    elif args.prog=="ORCA":
        dict["opt"]=="Opt"







if args.setup:


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
try:
    coords=open(args.crd, "r")
    crd_lines=coords.readlines()
except:
    print("No coordinates file specified. Continue at your own risk.")
    pass

###############Gaussian##################################
if args.prog == "Gaussian":
    lines.append("%Nprocs=" + dict["procs"] + "\n%Chk=" + dict["title"] + "\n%Mem=" +
    dict["mem"])
    lines.append("#p " + dict["task"] + " " + dict["XC"] + "/" + dict["basis"] + args.add + add_input + "\n\n")
    lines.append(dict["title"] + "\n\n")
    lines.append(dict["charge"] + " " + dict["multiplicity"] + "\n")
    try:
        for line in crd_lines:
            lines.append(line)
    except:
        pass
    lines.append("\n")
###########ADF#############################################
elif args.prog == "ADF":
    lines.append(dict["title"])
    lines.append("ATOMS\n")
    try:
        for line in crd_lines:
            lines.append(line)
    except:
        pass
    lines.append("END\n\n")


    #symmetry and Charge
    lines.append("SYMMETRY " + dict["symmetry"])
    lines.append("CHARGE " + dict["charge"] + " " + dict["multiplicity"])

    #geometry
    lines.append("GEOMETRY\n")
    lines.append("ITERATIONS " + dict["iterations"])
    lines.append("CONVERGE " + dict["converge"])
    lines.append("END\n\n")
    #scf
    lines.append("SCF\n")
    lines.append("ITERATIONS " + dict["iterations"])
    lines.append("CONVERGE " + dict["scf_converge"])
    lines.append("END\n\n")
    #functional
    lines.append("XC\n")
    lines.append(dict["XC"])
    lines.append("END\n\n")
    #basis
    lines.append("BASIS\n")
    lines.append("TYPE " + dict["basis"])
    lines.append(dict["core"])
    lines.append("END\n\n")
    #other
    lines.append("NUMERICALQUALITY " + dict["quality"])
    lines.append(dict["relativistic"])
    lines.append(args.add_input.replace('.','\n'))
    lines.append(add_input.replace('.','\n'))
    #END
    lines.append("\nEND INPUT")





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
