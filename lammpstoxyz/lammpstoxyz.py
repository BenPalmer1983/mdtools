"""
python3 lammpstoxyz.py dump.custom


"""

import numpy
import sys
import os




class lammpstoxyz:


  @staticmethod
  def main():
  
  
    if(len(sys.argv) < 2):
      print("Check arguments.")
      exit()
      
    file_in = sys.argv[1].strip()  
    
    if(not os.path.isfile(file_in)):
      print("File does not exist")
      exit()
    
    #fh_write = open('out.xyz', 'w')
    fh_write = None
    
    axes_xyz = [0,0,0,0,0,0]
    
    fh = open(file_in, 'r')
    n = 0
    axes = 0
    for line in fh:
      if(line.strip() == "ITEM: TIMESTEP" and axes == 0):
        if(n>0):
          lammpstoxyz.save(fh_write, coords, n, axes_xyz)
        coords = []
        n = n + 1
      elif(line.strip() == "ITEM: BOX BOUNDS pp pp pp" and axes == 0):
        axes = 3
      elif(axes > 0):
        f = line.strip().split(" ")
        if(axes == 3):
          axes_xyz[0] = float(f[0])
          axes_xyz[1] = float(f[1])
        elif(axes == 2):
          axes_xyz[2] = float(f[0])
          axes_xyz[3] = float(f[1])
        elif(axes == 1):
          axes_xyz[4] = float(f[0])
          axes_xyz[5] = float(f[1])
        axes = axes - 1
      else:
        f = line.strip().split(" ")
        if(len(f) == 5): 
          x = float(f[2]) - axes_xyz[0] 
          y = float(f[3]) - axes_xyz[2]
          z = float(f[4]) - axes_xyz[4]
          coords.append([f[1], x, y, z])
        #  print(f)
    fh.close()
    
    
    #fh_write.close()
    

      
      

  def save(fh, coords, n, axes_xyz):
    close = False
    if(fh == None):
      nstr = str(n)
      while(len(nstr) < 6):
        nstr = "0" + nstr
      fh = open('out_' + nstr + '.xyz', 'w')  
      close = True  
    a = axes_xyz[1] - axes_xyz[0]
    b = axes_xyz[3] - axes_xyz[2]
    c = axes_xyz[5] - axes_xyz[4]
    fh.write(str(len(coords)) + '\n')
    fh.write('Lattice="' + str(a) + ' 0.0 0.0 0.0 ' + str(b) + ' 0.0 0.0 0.0 ' + str(c) + '" #Time step ' + str(n) + '\n')
    for c in coords:
      fh.write(str(c[0]) + ' ' + str(c[1]) + ' ' + str(c[2]) + ' ' + str(c[3]) + '\n')

    if(close):
      fh.close()



lammpstoxyz.main()



"""
        nstr = str(n)
        while(len(nstr) < 6):
          nstr = "0" + nstr
          if(not one):    
            fh.close()
"""
