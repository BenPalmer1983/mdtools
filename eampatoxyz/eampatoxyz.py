import numpy
import sys
import os

#
#  python3 eampatoxyz.py in out
#
#

class eampatoxyz:


  @staticmethod
  def main():
  
      
    if(len(sys.argv) < 3):
      print("Check arguments.")
      exit()
      
    dir_in = sys.argv[1].strip()      
    dir_out = sys.argv[2].strip()
    
    if(not os.path.isdir(dir_in)):
      print("Dir does not exist")
      exit()
      
    os.makedirs(dir_out, exist_ok=True)  
      
    files = eampatoxyz.file_list(dir_in)
    
    for file_path in files:
      eampatoxyz.make_file(file_path, dir_out)


  
  @staticmethod
  def make_file(path_in, dir_out):
    file_name = os.path.basename(path_in)
    path_out = os.path.join(dir_out, file_name)
    
    uv = numpy.zeros((3,3,), dtype=numpy.float64,)
    coords = []
    
    fh = open(path_in, 'r')
    for line in fh:
      line = line.split("//")
      line = line[0]
      line = line.split("/*")
      line = line[0]
      line_p = eampatoxyz.one_space(line.replace('\t', ' ').strip())
      if(line.upper()[0:5] == "#ALAT"):        
        d = line_p.split(" ")
        a0 = float(d[1])
      elif(line.upper()[0:2] == "#X"):        
        d = line_p.split(" ")
        uv[0,0] = float(d[1])  
        uv[0,1] = float(d[2]) 
        uv[0,2] = float(d[3])       
      elif(line.upper()[0:2] == "#Y"):        
        d = line_p.split(" ")
        uv[1,0] = float(d[1])  
        uv[1,1] = float(d[2]) 
        uv[1,2] = float(d[3])     
      elif(line.upper()[0:2] == "#Z"):        
        d = line_p.split(" ")
        uv[2,0] = float(d[1])  
        uv[2,1] = float(d[2]) 
        uv[2,2] = float(d[3])    
      elif(line != ""):   
        if(line[0] != "#"):
          d = line_p.split(" ")
          if(len(d) == 4 or len(d) == 7):
            coords.append(d[0:4])        
    box = a0 * uv        
    fh.close()

    fh = open(path_out, 'w')
    fh.write(str(len(coords)) + "\n")
    fh.write('Lattice="')
    for i in range(3):
      for j in range(3):
        fh.write(str(box[i,j]))
        if(not (i == 2 and j == 2)):
          fh.write(' ')
    fh.write('"\n')  
    for c in coords:
      fh.write(c[0] + ' ' + str(c[1]) + ' ' + str(c[2]) + ' ' + str(c[3]) + '\n')  
    fh.close()
    
    


  @staticmethod
  def file_list(path_in, files=[]):
    for path in os.listdir(path_in):
      path_new = os.path.join(path_in, path)
      if(os.path.isdir(path_new)):
        files = cfile.file_list(path_new, files)
      else:
        files.append(path_new)
    return files


  @staticmethod
  def one_space(l):
    out = ''
    last = None
    for c in l:
      if(not (c == " " and last == " ")):
        out = out + c
      last = c
    return out


if __name__ == "__main__":
  eampatoxyz.main()    




