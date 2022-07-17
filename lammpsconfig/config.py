import os
import numpy
import sys
import random


"""
python3 config.py input.in

"""

class config:

  d = {
  # INPUT
  'output': 'config',
  'structure': None,
  'a0': None,
  'uv_in': numpy.zeros((3,3,), dtype=numpy.float64,),
  'copies': numpy.zeros((3,), dtype=numpy.int32,),
  'labels': [],
  'distribution': 'ORDERED',
  'x': numpy.asarray([0.0, 1.0], dtype=numpy.float64),
  'y': numpy.asarray([0.0, 1.0], dtype=numpy.float64),
  'z': numpy.asarray([0.0, 1.0], dtype=numpy.float64),  
  'offset': numpy.zeros((3,), dtype=numpy.float64,),
  # CALCULATED
  'uv': numpy.zeros((3,3,), dtype=numpy.float64,),
  'copies_mult': numpy.zeros((3,3,), dtype=numpy.float64,),
  'box': numpy.zeros((3,3,), dtype=numpy.float64,),
  'coords': None,
  'coords_labels': None,
  'coords_real': None,
  'count': 0,
  }


  @staticmethod
  def make():
    print("Example usage:")
    print("python3 config.py input.in")

    if(len(sys.argv) != 2):
      print("Check arguments.")
      exit()

    inpfile = sys.argv[1]
    if(not os.path.isfile(inpfile)):
      print("Input file does not exist.")
      exit()
      
    # Load input
    config.load(inpfile)

    # Make sim box
    config.make_box()

    # Make coords
    config.make_coords()

    # Make coords
    config.make_coords_real()

    # Make lammps file
    config.make_lammps_file()

    # Make lammps file
    config.make_crystal_file()


  def load(inpfile):
    print("Load input")
    fh = open(inpfile, 'r')
    for line in fh:
      line = line.strip()
      
      if("#OUTPUT" in line.upper()):
        f = line.split(" ")
        config.d['output'] = f[1]
      elif("#STRUCTURE" in line.upper()):
        f = line.split(" ")
        config.d['structure'] = f[1]
      elif("#A0" in line.upper()):
        f = line.split(" ")
        config.d['a0'] = float(f[1])
      elif("#BX" in line.upper()):
        f = line.split(" ")
        f = numpy.asarray(f[1].split(","), dtype=numpy.float64)
        config.d['uv_in'][0,:] = f[0:3]
      elif("#BY" in line.upper()):
        f = line.split(" ")
        f = numpy.asarray(f[1].split(","), dtype=numpy.float64)
        config.d['uv_in'][1,:] = f[0:3]
      elif("#BZ" in line.upper()):
        f = line.split(" ")
        f = numpy.asarray(f[1].split(","), dtype=numpy.float64)
        config.d['uv_in'][2,:] = f[0:3]
      elif("#COPIES" in line.upper()):
        f = line.split(" ")
        f = numpy.asarray(f[1].split(","), dtype=numpy.int32)
        config.d['copies'][:] = f[0:3]
      elif("#LABELS" in line.upper()):
        f = line.split(" ")
        config.d['labels'] = f[1].split(",")
      elif("#DIST" in line.upper()):
        f = line.split(" ")
        config.d['distribution'] = f[1].split(",")
      elif("#X" in line.upper()):
        f = line.split(" ")
        config.d['x'] = numpy.asarray(f[1].split(","), dtype=numpy.float64)
      elif("#Y" in line.upper()):
        f = line.split(" ")
        config.d['y'] = numpy.asarray(f[1].split(","), dtype=numpy.float64)
      elif("#Z" in line.upper()):
        f = line.split(" ")
        config.d['z'] = numpy.asarray(f[1].split(","), dtype=numpy.float64)
      elif("#OFFSET" in line.upper()):
        f = line.split(" ")
        f = numpy.asarray(f[1].split(","), dtype=numpy.float64)
        config.d['offset'][:] = f[0:3]


    fh.close()


  def make_box():
    print("Make box")
    config.d['copies_mult'][0,0] = float(config.d['copies'][0])
    config.d['copies_mult'][1,1] = float(config.d['copies'][1])
    config.d['copies_mult'][2,2] = float(config.d['copies'][2])
    config.d['uv'] = numpy.matmul(config.d['copies_mult'],config.d['uv_in']) 
    config.d['box'] = config.d['a0'] * config.d['uv']


  def make_coords():
    print("Make coords")
    coords_prim = config.structure(config.d['structure'])
    labels = []
    coords = []

    # Make coords
    for i in range(config.d['copies'][0]):
      for j in range(config.d['copies'][1]):
        for k in range(config.d['copies'][2]):
          for n in range(len(coords_prim)):
            coords.append([(i+coords_prim[n,0])/config.d['copies'][0], (j+coords_prim[n,1])/config.d['copies'][1], (k+coords_prim[n,2])/config.d['copies'][2]])


    if(config.d['distribution'][0].upper() == "ORDERED"): 
      for i in range(config.d['copies'][0]):
        for j in range(config.d['copies'][1]):
          for k in range(config.d['copies'][2]):
            for n in range(len(coords_prim)):
              labels.append(config.d['labels'][n % len(config.d['labels'])])
    elif(config.d['distribution'][0].upper() == "MIXED"): 
      ll_len = config.d['copies'][0] * config.d['copies'][1] * config.d['copies'][2] * len(coords_prim)
      t = 0
      lquant = []
      for n in range(1, len(config.d['distribution'])):
        t = t + int(config.d['distribution'][n])
        lquant.append(int(config.d['distribution'][n]))
      for n in range(len(lquant)):
        lquant[n] = int(ll_len * (lquant[n] / t))
      if(sum(lquant)<ll_len):
        lquant[0] = lquant[0] + 1      
      for n in range(len(lquant)):
        for m in range(lquant[n]):
          labels.append(config.d['labels'][n])
      random.shuffle(labels)

    # Apply cutoff
    labels_reduced = []
    coords_reduced = []
    
    for n in range(len(coords)):
      if(coords[n][0]>=config.d['x'][0] and coords[n][0]<=config.d['x'][1] 
         and coords[n][1]>=config.d['y'][0] and coords[n][1]<=config.d['y'][1] 
         and coords[n][2]>=config.d['z'][0] and coords[n][2]<=config.d['z'][1]): 
        labels_reduced.append(labels[n])
        coords_reduced.append(coords[n])
    
    
    # Save
    config.d['coords'] = numpy.asarray(coords_reduced, dtype=numpy.float64)
    config.d['coord_labels'] = labels_reduced
    config.d['count'] = len(config.d['coord_labels'])


  def make_coords_real():
    print("Make coords (real)")
    config.d['coords_real'] = numpy.copy(config.d['coords'])
    for n in range(config.d['count']):
      config.d['coords_real'][n,:] = config.d['offset'][:] + numpy.matmul(config.d['box'], config.d['coords'][n,:])


  def make_lammps_file():
    print("Make LAMMPS file")
    #os.makedirs(dir, exist_ok=True)
    levcfg = 2
    imcon = 3        
    fh = open(config.d['output'] + '.lammps.in', 'w')
    fh.write("# Created Config\n")
    fh.write("\n")
    fh.write(str(config.d['count']) + " atoms\n")
    fh.write(str(len(config.d['labels'])) + " atom types\n")
    fh.write("\n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(config.d['box'][0,0] + 2 * config.d['offset'][0]) + "  xlo xhi \n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(config.d['box'][1,1] + 2 * config.d['offset'][1]) +  "  ylo yhi \n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(config.d['box'][2,2] + 2 * config.d['offset'][2]) + "  zlo zhi \n")
    fh.write("\n")
    fh.write("Atoms\n")
    fh.write("\n")
    for n in range(config.d['count']):
      fh.write(config.padr(str(n+1), 6) + " ")
      fh.write(config.padr(str(config.d['coord_labels'][n]), 2) + " ")
      if(config.d['coords_real'][n,0] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords_real'][n,0])) + " ", 14))
      if(config.d['coords_real'][n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords_real'][n,1])) + " ", 14))
      if(config.d['coords_real'][n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords_real'][n,2])) + " ", 14))
      fh.write("\n")      
    fh.close()
    
  
  def make_crystal_file():
    print("Make crystal file")
    fh = open(config.d['output'] + '.crys', 'w')
    fh.write("#a0 {:.5e}\n".format(config.d['a0']))
    fh.write("#bx {:.5e} {:.5e} {:.5e}\n".format(config.d['uv'][0,0],config.d['uv'][0,1],config.d['uv'][0,2]))
    fh.write("#by {:.5e} {:.5e} {:.5e}\n".format(config.d['uv'][1,0],config.d['uv'][1,1],config.d['uv'][1,2]))
    fh.write("#bz {:.5e} {:.5e} {:.5e}\n".format(config.d['uv'][2,0],config.d['uv'][2,1],config.d['uv'][2,2]))
    fh.write("\n")

    for n in range(config.d['count']):
      #fh.write(config.padr(str(n+1), 6) + " ")
      fh.write(config.padr(str(config.d['coord_labels'][n]), 2) + " ")
      if(config.d['coords'][n,0] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords'][n,0])) + " ", 14))
      if(config.d['coords'][n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords'][n,1])) + " ", 14))
      if(config.d['coords'][n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(config.d['coords'][n,2])) + " ", 14))
      fh.write("\n")      
    fh.close()




  """
  def aa():
    print("python3 config.py 1,2 fcc 4.04 1,1,1,0,0,0 4,4,4 alexample",len(sys.argv))
    
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
            coords[m,:] = numpy.asarray([(i+coords_prim[n,0])/c[0], (j+coords_prim[n,1])/c[1], (k+coords_prim[n,2])/c[2]])
            m = m + 1

    levcfg = 2
    imcon = 3
    
    coords_real = numpy.zeros((len(coords_prim) * c[0] * c[1] * c[2], 3,), dtype=numpy.float64)
    for n in range(len(coords)):
      coords_real[n,:] = a0 * numpy.matmul(uv, coords[n,:])
    
    fh = open("config.in", 'w')
    fh.write("# Created Config\n")
    fh.write("\n")
    fh.write(str(len(coords_real)) + " atoms\n")
    fh.write(str(len(labels_prim)) + " atom types\n")
    fh.write("\n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(box[0,0]) + "  xlo xhi \n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(box[1,1]) + "  ylo yhi \n")
    fh.write("{0:.7f}".format(0.0) + "   " + "{0:.7f}".format(box[2,2]) + "  zlo zhi \n")
    fh.write("\n")
    fh.write("Atoms\n")
    fh.write("\n")
    for n in range(len(coords_real)):
      fh.write(config.padr(str(n+1), 6) + " ")
      fh.write(config.padr(str(labels[n]), 2) + " ")
      if(coords_real[n,0] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,0])) + " ", 14))
      if(coords_real[n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,1])) + " ", 14))
      if(coords_real[n,1] >= 0.0):
        fh.write(" ")        
      fh.write(config.padr(str("{0:.7e}".format(coords_real[n,2])) + " ", 14))
      fh.write("\n")      
    fh.close()
  """  

  @staticmethod
  def structure(structure):
    if(structure=='fcc'):
      return numpy.asarray([[0.0, 0.0, 0.0], [0.5, 0.5, 0.0], [0.5, 0.0, 0.5], [0.0, 0.5, 0.5]])
    elif(structure=='bcc'):
      return numpy.asarray([[0.0, 0.0, 0.0], [0.5, 0.5, 0.5]])
    elif(structure=='sc'):
      return numpy.asarray([[0.0, 0.0, 0.0]])
    elif(structure=='hcp'):
      return numpy.asarray([[0.0, 0.0, 0.0], [0.3333333, 0.6666667, 0.5]])
    elif(structure=='c-fcc'):
      return numpy.asarray([[0.25, 0.25, 0.25], [0.75, 0.75, 0.25], [0.75, 0.25, 0.75], [0.25, 0.75, 0.75]])
    elif(structure=='c-bcc'):
      return numpy.asarray([[0.25, 0.25, 0.25], [0.75, 0.75, 0.75]])
    elif(structure=='c-sc'):
      return numpy.asarray([[0.5, 0.5, 0.5]])
    elif(structure=='c-hcp'):
      return numpy.asarray([[0.3333333,0.1666667,0.2500000],[0.6666667,0.8333333,0.7500000]])





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



