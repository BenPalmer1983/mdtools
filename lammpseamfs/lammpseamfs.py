import numpy
import matplotlib.pyplot as plt

class lammpseamfs:

  @staticmethod
  def run():
    #lammpseamfs.read('Fe_2.eam.fs.txt')
    #lammpseamfs.read('Ru.eam.fs')
    #lammpseamfs.read('Fe_Earth_core.eam.fs')
    #lammpseamfs.read('Fe.eam.fs')
    lammpseamfs.read('Fe_5.eam.fs')



  

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
      if(n == 4):
        f = d[n].split(" ")
        fd['nrho'] = int(f[0])
        fd['drho'] = float(f[1])
        fd['nr'] = int(f[2])
        fd['dr'] = float(f[3])
        fd['f'].append(numpy.zeros((fd['nrho'],2,),))
        fd['f'].append(numpy.zeros((fd['nrho'],2,),))
        fd['f'].append(numpy.zeros((fd['nrho'],2,),))
        
        fd['f'][0][:,0] = numpy.linspace(0.0, (fd['nrho'] - 1) * fd['drho'], fd['nrho'])
        fd['f'][1][:,0] = numpy.linspace(0.0, (fd['nr'] - 1) * fd['dr'], fd['nr'])
        fd['f'][2][:,0] = numpy.linspace(0.0, (fd['nr'] - 1) * fd['dr'], fd['nr'])
      elif(n > 5):
        f = d[n].split(" ")
        if(len(f) >= 1):
          fd['f'][k][m,1] = float(f[0])
        if(len(f) >= 2):
          fd['f'][k][m+1,1] = float(f[1])
        if(len(f) >= 3):
          fd['f'][k][m+2,1] = float(f[2])
        if(len(f) >= 4):
          fd['f'][k][m+3,1] = float(f[3])
        if(len(f) >= 5):
          fd['f'][k][m+4,1] = float(f[4])
        m = m + 5
        if(m >= fd['nrho']):
          m = 0
          k = k + 1
       
    for n in range(len(fd['f'][2][:,0])):
      if(fd['f'][2][n,0] == 0.0):
        fd['f'][2][n,1] = 0.0
      else:
        fd['f'][2][n,1] = fd['f'][2][n,1] / fd['f'][2][n,0]
  
 
    plt.plot(fd['f'][0][:,0], fd['f'][0][:,1])
    plt.ylim(-100.0, 100)
    plt.savefig('embe.eps')
    plt.cla()  
    numpy.savetxt('embe.tab', fd['f'][0][:,:])
    
    plt.plot(fd['f'][1][:,0], fd['f'][1][:,1])
    plt.ylim(-1.0, 100)  
    plt.savefig('dens.eps')
    plt.cla()    
    numpy.savetxt('dens.tab', fd['f'][1][:,:])  
    
    plt.plot(fd['f'][2][:,0], fd['f'][2][:,1])
    plt.ylim(-1.0, 100)
    plt.savefig('pair.eps')
    plt.cla()
    numpy.savetxt('pair.tab', fd['f'][2][:,:])  


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
