




class dlpolytoxyz:

  @staticmethod
  def run():

    hfile = "/home/ben/dlpoly/rutest/HISTORY"
    outfile = "history.xyz"

    h = []
    fh = open(hfile, 'r')
    for line in fh:
      h.append(dlpolytoxyz.one_space(line.strip()))
    fh.close()


    fh = open(outfile, 'w')
    n = 0
    ts = None
    while(n < len(h)):
      if(h[n][0:8] == "timestep"):
        f = h[n].split(" ")
        ts = int(f[1])
        nat = int(f[2])
        fh.write(str(nat) + '\n\n')
        n = n + 4
        for m in range(nat): 
          f = h[n].split(" ")
          fh.write(f[0] + ' ')
          f = h[n+1].split(" ")
          fh.write("{0:.5e}".format(float(f[0])) + ' ')
          fh.write("{0:.5e}".format(float(f[1])) + ' ')
          fh.write("{0:.5e}".format(float(f[2])) + '\n')
          n = n + 2
        n = n - 1
      n = n + 1
    fh.close()

    
  @staticmethod
  def one_space(l):
    out = ''
    last = None
    for c in l:
      if(not (c == " " and last == " ")):
        out = out + c
      last = c
    return out

dlpolytoxyz.run()
