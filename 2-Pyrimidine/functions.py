#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# MIT License
#
# Copyright (c) 2018  Paul Bauer <paul.bauer.q@gmail.com>
# Beer Ware Licence
#
# Backup function Copyright (c) 2017 Miha Purg <miha.purg@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
#
# Helper functions for tutorial

def backup(dirname):
    import os
    import shutil
    """Check if a file exists, make a backup (#filename.1#, #filename.2#...).
    
    Args:
        dirname (string):  name of dir to backup
    Returns:
        backup_dirname (string):  basename of the new filename or empty
                                       string if the file was not found.
    """
    if os.path.lexists(dirname):
        di = os.path.dirname(dirname)
        sd = os.path.basename(dirname)
        backup_dirname = sd
        i = 1
        while os.path.lexists(os.path.join(di,backup_dirname)):
            backup_dirname = "#%s.%d#" % (sd,i)
            i += 1
            if i > 10:
                print("You have more than 100 backed up files... ")
        shutil.move(dirname, backup_dirname)
        return backup_dirname
    
    return ""

def which(program):
    """Check if an executable file of this name exists.

    Args:
        program (string):  name of executable file to check
    Returns:
        nothing
    """
    import os
    def is_exe(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)

    fpath, fname = os.path.split(program)
    if fpath:
        if is_exe(program):
            return program
    else:
        for path in os.environ["PATH"].split(os.pathsep):
            exe_file = os.path.join(path, program)
            if is_exe(exe_file):
                return exe_file

    return None

def writemdpfile(position = 0, filename = "", kind = 0, group1name = "PYR1", group2name = "PYR2"):
    """Write the correct mdp file for a certain simulation and umbrella window.

    Args:
        position (real): Value for the sampling coordinate.
        filename (string): Name for the file written out.
        kind (enum): What kind of mdp file to write.
        group1name (string): Name for the first group in COM pulling.
        group2name (string): Name for second group in COM pulling.
                     0 - Minimzation
                     1 - Unrestrained minimization
                     2 - NVT equilibration
                     3 - NPT equilibration
                     4 - MD simulation
    Returns:
        Nothing
    """
    if (filename == ""):
        print("Not a valid filename, we are out of here")
        return None

    if kind == 0:
        line = """
define                   = -DFLEXIBLE
integrator               = steep
nsteps                   = 1000
emtol                    = 500
nstenergy                = 500
nstlog                   = 500
nstxout-compressed       = 1000

constraint-algorithm     = lincs
constraints              = h-bonds

cutoff-scheme            = Verlet

coulombtype              = PME
rcoulomb                 = 1.0

vdwtype                  = Cut-off
rvdw                     = 1.0
DispCorr                 = EnerPres

pull                     = yes
pull-ngroups             = 2\n"""
        line = line +"pull-group1-name         = "+str(group1name)
        line = line +"\npull-group2-name         = "+str(group2name)+"\n"
        line = line +"""pull-ncoords             = 1
pull-coord1-type         = umbrella
pull-coord1-geometry     = distance
pull-coord1-groups       = 1 2
pull-coord1-k            = 5000.0
pull-coord1-rate         = 0.0\n"""
        line = line + "pull-coord1-init         = "+str(position)
        line = line + "\npull-coord1-start        = no"
    elif kind == 1:
        line = """
integrator               = steep
nsteps                   = 50000
emtol                    = 500

nstenergy                = 500
nstlog                   = 500
nstxout-compressed       = 1000

cutoff-scheme            = Verlet

coulombtype              = PME
rcoulomb                 = 1.0

vdwtype                  = Cut-off
rvdw                     = 1.0
DispCorr                 = EnerPres

pull                     = yes
pull-ngroups             = 2\n"""
        line = line +"pull-group1-name         = "+str(group1name)
        line = line +"\npull-group2-name         = "+str(group2name)+"\n"
        line = line +"""pull-ncoords             = 1
pull-coord1-type         = umbrella
pull-coord1-geometry     = distance
pull-coord1-groups       = 1 2
pull-coord1-k            = 5000.0
pull-coord1-rate         = 0.0\n"""
        line = line + "pull-coord1-init         = "+str(position)
        line = line +"\npull-coord1-start        = no"
    elif kind == 2:
        line = """
integrator               = md        
dt                       = 0.002     ; 2 fs
nsteps                   = 50000     ; 100 ps

nstenergy                = 200
nstlog                   = 2000
nstxout-compressed       = 10000

gen-vel                  = yes
gen-temp                 = 298.15

constraint-algorithm     = lincs
constraints              = h-bonds

cutoff-scheme            = Verlet

coulombtype              = PME
rcoulomb                 = 1.0

vdwtype                  = Cut-off
rvdw                     = 1.0
DispCorr                 = EnerPres

tcoupl                   = Nose-Hoover
tc-grps                  = System
tau-t                    = 2.0
ref-t                    = 298.15
nhchainlength            = 1

pull                     = yes
pull-ngroups             = 2\n"""
        line = line +"pull-group1-name         = "+str(group1name)
        line = line +"\npull-group2-name         = "+str(group2name)+"\n"
        line = line +"""pull-ncoords             = 1
pull-coord1-type         = umbrella
pull-coord1-geometry     = distance
pull-coord1-groups       = 1 2
pull-coord1-k            = 5000.0
pull-coord1-rate         = 0.0\n"""
        line = line + "pull-coord1-init         = "+str(position)
        line = line + "\npull-coord1-start        = no"
    elif kind == 3:
        line ="""

integrator               = md        
dt                       = 0.002     ; 2 fs
nsteps                   = 500000    ; 1.0 ns

nstenergy                = 200
nstlog                   = 2000
nstxout-compressed       = 10000

continuation             = yes
constraint-algorithm     = lincs
constraints              = h-bonds

cutoff-scheme            = Verlet
rlist                    = 1.0

coulombtype              = PME
rcoulomb                 = 1.0

vdwtype                  = Cut-off
rvdw                     = 1.0
DispCorr                 = EnerPres

tcoupl                   = Nose-Hoover
tc-grps                  = System
tau-t                    = 2.0
ref-t                    = 298.15
nhchainlength            = 1

pcoupl                   = Parrinello-Rahman 
tau_p                    = 2.0
compressibility          = 4.46e-5
ref_p                    = 1.0 

pull                     = yes
pull-ngroups             = 2\n"""
        line = line +"pull-group1-name         = "+str(group1name)
        line = line +"\npull-group2-name         = "+str(group2name)+"\n"
        line = line +"""pull-ncoords             = 1
pull-coord1-type         = umbrella
pull-coord1-geometry     = distance
pull-coord1-groups       = 1 2
pull-coord1-k            = 5000.0
pull-coord1-rate         = 0.0\n"""
        line = line + "pull-coord1-init         = "+str(position)
        line = line + "\npull-coord1-start        = no"
    elif kind == 4:
        line = """

integrator               = md
dt                       = 0.002     ; 2 fs
nsteps                   = 2500000   ; 5.0 ns

nstenergy                = 5000
nstlog                   = 5000
nstxout-compressed       = 2000

continuation             = yes
constraint-algorithm     = lincs
constraints              = h-bonds

cutoff-scheme            = Verlet

coulombtype              = PME
rcoulomb                 = 1.0

vdwtype                  = Cut-off
rvdw                     = 1.0
DispCorr                 = EnerPres

tcoupl                   = Nose-Hoover
tc-grps                  = System
tau-t                    = 2.0
ref-t                    = 298.15
nhchainlength            = 1

pcoupl                   = Parrinello-Rahman
tau_p                    = 2.0
compressibility          = 4.46e-5
ref_p                    = 1.0

pull                     = yes
pull-ngroups             = 2\n"""
        line = line +"pull-group1-name         = "+str(group1name)
        line = line +"\npull-group2-name         = "+str(group2name)+"\n"
        line = line +"""pull-ncoords             = 1
pull-coord1-type         = umbrella
pull-coord1-geometry     = distance
pull-coord1-groups       = 1 2
pull-coord1-k            = 5000.0
pull-coord1-rate         = 0.0\n"""
        line = line + "pull-coord1-init         = "+str(position)
        line = line + "\npull-coord1-start        = no"
    else:
        print("Unrecognized type for file writeout, doing nothing")
        return None
    filename = filename+".mdp"
    outfile = open(filename, "w")
    outfile.writelines(line)
    outfile.close()

def rungrompp(mdpname = "", prevname = "", maxwarn = 0):
    import subprocess
    """Run grompp on a an provided mdp file to generate the tpr.

    Args:
        mdpname (string): Name of the input mdp, as well as name of output tpr
        prevname (string): Name of additional input files for input (e.g. structure, restart files.
                           If empty, use default hardcoded name.
        maxwarn (integer): Number for maxwarn option of grompp, only set if you know what you are doing.
    Return:
        nothing
    """
    if (mdpname == ""):
        print("The name for the mdpfile can not be empty")
        return None

    commandlist = ["gmx", "grompp", "-n", "index.ndx", "-p", "topol.top"]
    commandlist.append("-f")
    commandlist.append(mdpname)
    commandlist.append("-o")
    commandlist.append(mdpname)
    commandlist.append("-pp")
    commandlist.append(mdpname)
    commandlist.append("-po")
    commandlist.append(mdpname+"out")
    commandlist.append("-c")
    if (prevname == ""):
        commandlist.append("ions")
    else:
        commandlist.append(prevname)
        commandlist.append("-t")
        commandlist.append(prevname)
    if (maxwarn > 0):
        commandlist.append("-maxwarn")
        commandlist.append(str(maxwarn))
    subprocess.check_call(commandlist)

def runmdrun(name = ""):
    """Execute actual mdrun process to run a simulation.

    Args:
        name (string): Input tpr file name to use for calculation.
    Returns:
        nothing
    """
    import subprocess
    commandlist = ["gmx", "mdrun", "-deffnm" , "-v"]
    commandlist.append(name)
    commandlist.append("-pf")
    commandlist.append("pullf-"+name)
    commandlist.append("-px")
    commandlist.append("pullx-"+name)

    subprocess.check_call(commandlist)



def umbrella(windows = 25, production = False, maxdist = 2.5, mindist = 0.05, filepath = "0-files", group1name = "PYR1", group2name = "PYR2"):
    import os
    import shutil
    """Run the umbrella sampling simulations to obtain a free energy profile.

    Args:
        windows (integer):  number of umbrella sampling windows to generate and run
        production (boolean): run an actual prodcution simulation
        maxdist (real): maximum separation to reach, in Å
        mindist (real): minimum separation to start from, in Å
        filepath (string): Path to input files for lookup.
        group1name (string): Name for first COM pulling group.
        group2name (string): Name for second COM pulling group.
    Returns:
        nothing
    """
    separation = (maxdist - mindist)/windows
    cwd = os.getcwd()

    for num in range (0, windows):
        dirname = "run-"+str(num)
        backup(dirname)
        os.mkdir(dirname)
        os.chdir(dirname)
        copyfiles = ["index.ndx", "ions.gro", "topol.top"]
        for files in copyfiles:
            path = filepath+"/"+str(files)
            shutil.copy2(path,os.getcwd())
        umbrellaposition = mindist + num*separation
        minname = "min."+str(num)
        min2name = "min2."+str(num)
        eqlname = "eql."+str(num)
        eql2name = "eql2."+str(num)
        prdname = "prd."+str(num)
        writemdpfile(umbrellaposition, minname, 0, group1name, group2name)
        if (production):
            rungrompp(minname)
            runmdrun(minname)
        writemdpfile(umbrellaposition, min2name, 1, group1name, group2name)
        if (production):
            rungrompp(min2name, minname, 1)
            runmdrun(min2name)
        writemdpfile(umbrellaposition, eqlname, 2, group1name, group2name)
        if (production):
            rungrompp(eqlname, min2name)
            runmdrun(eqlname)
        writemdpfile(umbrellaposition, eql2name, 3, group1name, group2name)
        if (production):
            rungrompp(eql2name, eqlname)
            runmdrun(eql2name)
        writemdpfile(umbrellaposition, prdname, 4, group1name, group2name)
        if(production):
            rungrompp(prdname, eql2name)
            runmdrun(prdname)
        # all done, go back and continue with the next window
        os.chdir(cwd)

def writetopfile(name = "topol.top", dirname = ""):
    """Write topology file to disk

    Args:
        name (string): file name of topology.
        dirname (string): name of top directory to look for files.
    Returns:
        nothing
    """
    ffstring = "#include \""+dirname+"/0-files/oplsaa.ff/forcefield.itp\""
    waterstring = "#include \""+dirname+"/0-files/oplsaa.ff/tip4p.itp\""
    ionstring = "#include \""+dirname+"/0-files/oplsaa.ff/ions.itp\""
    pyrstring = "#include \""+dirname+"/0-files/pyrimidine.itp\""
    line = """;
;	Hand made topology files
;

; Include forcefield parameters"""
    line = line + "\n"+ffstring
    line = line + "\n"+"""
; Include water topology"""
    line = line + "\n"+waterstring
    line = line + "\n"+"""
#ifdef POSRES_WATER
; Position restraint for each water oxygen
[ position_restraints ]
;  i funct       fcx        fcy        fcz
   1    1       1000       1000       1000
#endif

; Include topology for ions"""
    line = line + "\n"+ionstring
    line = line + "\n"+"""
; Include topology for pyrimidine"""
    line = line + "\n"+pyrstring
    line = line + "\n"+"""
[ system ]
; Name
2 Pyrimidine molecules

[ molecules ]
; Compound        #mols
pyrimidine 2\n"""

    outfile = open(name, "w")
    outfile.writelines(line)
    outfile.close()

def listdirectory(dirname = "."):
    """List files in the current directory

    Args:
        dirname (string): Name of the directory to check, default is current directory.
    Returns:
        nothing
    """
    import os

    filelist = os.listdir(dirname)
    for entry in filelist:
        print (entry)
