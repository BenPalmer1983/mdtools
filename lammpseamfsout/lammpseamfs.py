import numpy
import matplotlib.pyplot as plt
import sys
import os

class lammpseamfs:

  @staticmethod
  def run():
    if(len(sys.argv)<2):
      print("Give file path.")
      print("e.g. python3 lammpseamfs.py Al.lammps.eam")
      exit()
    fn = sys.argv[1]
    if(not os.path.isfile(fn)):
      print("File does not exist")
      exit()
    lammpseamfs.read(fn)



  

  @staticmethod
  def read(fn):
    fd = {
           'nrho': None, 
           'drho': None, 
           'nr': None, 
           'dr': None, 
           'cutoff': None, 
           'f': [], 
         }

    d = []
    fh = open(fn, 'r')
    for line in fh:
      d.append(lammpseamfs.one_space(line.strip()))
    fh.close()    

    m = 0
    k = 0
    for n in range(len(d)):
      if(n == 3):
        f = d[n].split(" ")
        ecount = int(f[0])
        elist = f[1:]
      elif(n == 4):
        f = d[n].split(" ")
        fd['nrho'] = int(f[0])
        fd['drho'] = float(f[1])
        fd['nr'] = int(f[2])
        fd['dr'] = float(f[3])
        
        rho_axis = numpy.linspace(0.0, (fd['nrho'] - 1) * fd['drho'], fd['nrho'])
        r_axis = numpy.linspace(0.0, (fd['nr'] - 1) * fd['dr'], fd['nr'])
        
        if(ecount == 1):
          fd['f'].append(numpy.zeros((fd['nrho'],2,),))   # Embe
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Density
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Pair
          
          fd['f'][0][:,0] = rho_axis[:]
          fd['f'][1][:,0] = r_axis[:]
          fd['f'][2][:,0] = r_axis[:]
        
        elif(ecount == 2):
          fd['f'].append(numpy.zeros((fd['nrho'],2,),))   # Embe A
          fd['f'].append(numpy.zeros((fd['nrho'],2,),))   # Embe B
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Density A
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Density B
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Pair A A
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Pair A B
          fd['f'].append(numpy.zeros((fd['nr'],2,),))     # Pair B B
        datapoints = fd['nrho']
    
    # Read blocks into embe, dens, pair
    embe = []
    dens = []
    pair = []
    blocks = []
    if(ecount == 1):
      blocks.append(d[6:207])
      blocks.append(d[207:408])
      blocks.append(d[408:609])
      
      dp = numpy.zeros((len(rho_axis), 2,), dtype=numpy.float64)
      dp[:,0] = rho_axis
      dp[:,1] = lammpseamfs.read_block(blocks[0])
      embe.append(dp)
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[1])
      dens.append(dp)      
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[2])
      dp = lammpseamfs.process_pair(dp)
      pair.append(dp)
      
    if(ecount == 2):
      blocks.append(d[6:207])
      blocks.append(d[207:408])
      blocks.append(d[409:610])
      blocks.append(d[610:811])
      blocks.append(d[811:1012])
      blocks.append(d[1012:1213])
      blocks.append(d[1213:1414])
      
      dp = numpy.zeros((len(rho_axis), 2,), dtype=numpy.float64)
      dp[:,0] = rho_axis
      dp[:,1] = lammpseamfs.read_block(blocks[0])
      embe.append(dp)
            
      dp = numpy.zeros((len(rho_axis), 2,), dtype=numpy.float64)
      dp[:,0] = rho_axis
      dp[:,1] = lammpseamfs.read_block(blocks[2])
      embe.append(dp)
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[1])
      dens.append(dp)     
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[3])
      dens.append(dp)        
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[4])
      dp = lammpseamfs.process_pair(dp)
      pair.append(dp)   
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[5])
      dp = lammpseamfs.process_pair(dp)
      pair.append(dp)   
            
      dp = numpy.zeros((len(r_axis), 2,), dtype=numpy.float64)
      dp[:,0] = r_axis
      dp[:,1] = lammpseamfs.read_block(blocks[6])
      dp = lammpseamfs.process_pair(dp)
      pair.append(dp)

      
    for i in range(len(embe)):
      fn = elist[i] + "_embe"
      lammpseamfs.write_files(fn, embe[i])
    for i in range(len(dens)):
      fn = elist[i] + "_dens"
      lammpseamfs.write_files(fn, dens[i])
    if(ecount == 1):
      fn = elist[0] + "_" + elist[0] + "_pair"
      lammpseamfs.write_files(fn, pair[0])
    if(ecount == 2):
      fn = elist[0] + "_" + elist[0] + "_pair"
      lammpseamfs.write_files(fn, pair[0])
      fn = elist[0] + "_" + elist[1] + "_pair"
      lammpseamfs.write_files(fn, pair[1])
      fn = elist[1] + "_" + elist[1] + "_pair"
      lammpseamfs.write_files(fn, pair[2])
      
      
      

  @staticmethod
  def process_pair(dp):
    for n in range(len(dp[:,0])):
      if(dp[n,0] == 0.0):
        dp[n,1] = 0.0
      else:
        dp[n,1] = dp[n,1] / dp[n,0]    
    return dp  
      
    
  @staticmethod
  def write_files(fn, dp): 
    r = numpy.amax(dp[:,1]) - numpy.amin(dp[:,1]) 
    ymin = max(numpy.amin(dp[:,1]) - 0.05 * r, -100.0)
    ymax = min(numpy.amax(dp[:,1]) + 0.05 * r, 100.0)
    plt.plot(dp[:,0], dp[:,1])
    plt.ylim(ymin, ymax)
    plt.savefig(fn + '.eps')
    plt.cla()  
    numpy.savetxt(fn + '.tab', dp[:,:])
    fh1 = open(fn + '.pot', 'w')
    fh1.write("#TYPE tab\n")
    fh2 = open(fn + '.tab', 'r')
    for line in fh2:
      fh1.write(line)
    fh2.close()
    fh1.close()
      
    
  @staticmethod
  def read_block(b):    
    temp = []
    for n in range(len(b)):
      f = b[n].split(" ")
      for fn in f:
        temp.append(float(fn))
    return numpy.asarray(temp, dtype=numpy.float64)

  @staticmethod
  def one_space(l):
    out = ''
    last = None
    for c in l:
      if(not (c == " " and last == " ")):
        out = out + c
      last = c
    return out


lammpseamfs.run()
