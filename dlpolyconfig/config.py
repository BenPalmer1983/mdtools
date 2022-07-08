import os
import numpy
import sys

class config:

  @staticmethod
  def make():
    print("Example usage:")
    print("python3 config.py al,ni fcc 4.04 1,1,1,0,0,0 4,4,4 alexample",len(sys.argv))
    
    if(len(sys.argv) != 7):
      print("Check arguments.")
      exit()
    
    try:
      labels_prim = sys.argv[1].split(",")
      structure = sys.argv[2].lower()
      a0 = float(sys.argv[3])
      uv6 = sys.argv[4].split(",")
      c = sys.argv[5].split(",")
      out = sys.argv[6]
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
            coords[m,:] = numpy.asarray([(i+coords_prim[n,0])/c[0]-0.5, (j+coords_prim[n,1])/c[1]-0.5, (k+coords_prim[n,2])/c[2]-0.5])
            m = m + 1

    levcfg = 2
    imcon = 3
    
    coords_real = numpy.zeros((len(coords_prim) * c[0] * c[1] * c[2], 3,), dtype=numpy.float64)
    for n in range(len(coords)):
      coords_real[n,:] = a0 * numpy.matmul(uv, coords[n,:])
    
    fh = open("CONFIG", 'w')
    fh.write("\n")
    fh.write("   " + str(levcfg) + "    " + str(imcon) + "    " + str(len(coords)) + " \n")
    fh.write("   " + "{0:.7f}".format(box[0,0]) + "    " + "{0:.7f}".format(box[0,1]) + "    " + "{0:.7f}".format(box[0,2]) + " \n")
    fh.write("   " + "{0:.7f}".format(box[1,0]) + "    " + "{0:.7f}".format(box[1,1]) + "    " + "{0:.7f}".format(box[1,2]) + " \n")
    fh.write("   " + "{0:.7f}".format(box[2,0]) + "    " + "{0:.7f}".format(box[2,1]) + "    " + "{0:.7f}".format(box[2,2]) + " \n")
    for n in range(len(coords)):
      config.write_atom(fh, labels[n], n+1)
      config.write_line(fh, coords_real[n, 0], coords_real[n, 1], coords_real[n, 2])
      config.write_line(fh, 0.0, 0.0, 0.0)
      config.write_line(fh, 0.0, 0.0, 0.0)
    fh.close()
    

  @staticmethod
  def structure(structure):
    if(structure=='fcc'):
      return numpy.asarray([[0.25, 0.25, 0.25], [0.75, 0.75, 0.25], [0.75, 0.25, 0.75], [0.25, 0.75, 0.75]])


  @staticmethod
  def write_atom(fh, label, n):
    label = config.padr(label, 8)
    n = config.padl(str(n), 10)
    line = config.padr(label + n, 72)
    fh.write(line + "\n")
    
    
  @staticmethod
  def write_line(fh, a, b, c):
    a = "{0:.5e}".format(a)
    b = "{0:.5e}".format(b)
    c = "{0:.5e}".format(c)
    line = config.padr(config.padl(a, 20) + config.padl(b, 20) + config.padl(c, 20), 72)
    fh.write(line + "\n")
    
    
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



