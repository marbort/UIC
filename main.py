import os, sys, subprocess, shutil, argparse

parser=argparse.ArgumentParser(description="Input Data")
parser.add_argument( 'program', type=str, help='Define for which program the input is needed',)
parser.add_argument( '--setup', dest='setup', type=str, help='initialize guided setup', default="")
parser.add_argument( '--calc', dest='calc', type=str, help='calculation type', default="opt")
parser.add_argument( '--bas', dest='bas', type=str, help='basis set type', default="6-31G")
parser.add_argument( '--funct', dest='funct', type=str, help='functional type', default="BLYP")
parser.add_argument( '--title', dest='title', type=str, help='job name', default="MOLECULE")
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
