import os
import numpy
import sys

"""
python3 makecoords.py Fe1,Fe2 fcc 4.04 1,1,1,0,0,0 4,4,4 fe_bulk

"""


class config:

  @staticmethod
  def make():
    print("Example usage:")
    print("python3 makecoords.py 1,2 fcc 4.04 1,1,1,0,0,0 4,4,4 alexample cube,0.0,1.0,0.0,1.0,0.0,0.5",len(sys.argv))
    print("python3 makecoords.py Al fcc 4.04 1,1,1,0,0,0 4,4,4 al_slab",len(sys.argv))
    
    if(len(sys.argv) < 7):
      print("Check arguments.")
      exit()
    
    try:
      labels_prim = sys.argv[1].split(",")
      structure = sys.argv[2].lower()
      a0 = float(sys.argv[3])
      uv6 = sys.argv[4].split(",")
      c = sys.argv[5].split(",")
      out = sys.argv[6]
      #shapes = sys.argv[7:]
    except:
      print("Check input arguments")
      exit()
        
    c = numpy.asarray(c, dtype=numpy.int)  
    uv = numpy.zeros((3,3,), dtype=numpy.float64)
    uv[0,0] = uv6[0]
    uv[1,1] = uv6[1]
    uv[2,2] = uv6[2]
    uv[0,1] = uv6[5]
    uv[1,0] = uv6[5]
    uv[0,2] = uv6[4]
    uv[2,0] = uv6[4]
    uv[1,2] = uv6[3]
    uv[2,1] = uv6[3]
    cm = numpy.zeros((3,3,), dtype=numpy.float64)
    cm[0,0] = c[0]
    cm[1,1] = c[1]
    cm[2,2] = c[2]
    uv = numpy.matmul(cm,uv) 
    box = a0 * uv
    
    print("Labels:     ", labels_prim)
    print("Structure:  ", structure)
    print("a0:         ", a0)
    print("uv:         ", uv[0,:])
    print("            ", uv[1,:])
    print("            ", uv[2,:])
    print("c:          ", c)
    
    coords_prim = config.structure(structure)
    labels = []
    coords = numpy.zeros((len(coords_prim) * c[0] * c[1] * c[2], 3,), dtype=numpy.float64)
    
    m = 0
    for i in range(c[0]):
      for j in range(c[1]):
        for k in range(c[2]):
          for n in range(len(coords_prim)):
            labels.append(labels_prim[n % len(labels_prim)])
            coords[m,:] = numpy.asarray([(i+coords_prim[n,0])/c[0], (j+coords_prim[n,1])/c[1], (k+coords_prim[n,2])/c[2]])
            m = m + 1
            
    zedge_lower = 0.0
    zedge_upper = 1.0
    
    coords_real = numpy.zeros((len(coords_prim) * c[0] * c[1] * c[2], 3,), dtype=numpy.float64)
    for n in range(len(coords)):
      coords_real[n,:] = a0 * numpy.matmul(uv, coords[n,:])
    
    fh = open("coords_real.in", 'w')
    for n in range(len(coords_real)):
      fh.write(config.padr(str(labels[n]), 10) + " ")
      if(coords_real[n,0] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,0])) + " ", 14))
      if(coords_real[n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,1])) + " ", 14))
      if(coords_real[n,2] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,2])) + " ", 14))
      fh.write("\n")      
    fh.close()
    
    m = 0
    fh = open("coords.in", 'w')
    for n in range(len(coords)):
      if(coords[n,2] >= zedge_lower and coords[n,2] <= zedge_upper):
        m = m + 1
        fh.write(config.padr(str(labels[n]), 10) + " ")
        if(coords[n,0] >= 0.0):
          fh.write(" ")        
        fh.write(config.padr(str("{0:.7e}".format(coords[n,0])) + " ", 14))
        if(coords[n,1] >= 0.0):
          fh.write(" ")        
        fh.write(config.padr(str("{0:.7e}".format(coords[n,1])) + " ", 14))
        if(coords[n,2] >= 0.0):
          fh.write(" ")        
        fh.write(config.padr(str("{0:.7e}".format(coords[n,2])) + " ", 14))
        fh.write("\n")      
    fh.close()
    print(m)
    
    fh = open("coords_forces.in", 'w')
    for n in range(len(coords)):
      fh.write(config.padr(str(labels[n]), 10) + " ")
      if(coords[n,0] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords[n,0])) + " ", 14))
      if(coords[n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords[n,1])) + " ", 14))
      if(coords[n,2] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords[n,2])) + " ", 14))
      fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(0.0)) + " ", 14))
      fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(0.0)) + " ", 14))
      fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(0.0)) + " ", 14))
      fh.write("\n")      
    fh.close()
    

  @staticmethod
  def structure(structure):
    if(structure=='fcc'):
      return numpy.asarray([[0.25, 0.25, 0.25], [0.75, 0.75, 0.25], [0.75, 0.25, 0.75], [0.25, 0.75, 0.75]])
      #return numpy.asarray([[0.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])


    
    
  @staticmethod
  def padl(inp, plen=17):
    while(len(inp) < plen):
       inp = " " + inp
    return inp
    
  @staticmethod
  def padr(inp, plen=17):
    while(len(inp) < plen):
       inp = inp + " "
    return inp
    
config.make()



