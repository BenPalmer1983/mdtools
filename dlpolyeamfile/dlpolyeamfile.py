import numpy


class dlpolyeamfile:


  def run():
    pair = numpy.loadtxt('Al_plot.pair')
    dens = numpy.loadtxt('Al_plot.den')
    embe = numpy.loadtxt('Al_plot.embed')


    print(pair)
    print(dens)
    print(embe)


    fh = open("TABEAM", 'w')
    fh.write("AL EAM\n")
    fh.write("3\n")
    
    fh.write("pair Al Al ")
    fh.write(str(len(pair)) + " " + str(pair[0, 0]) + " " + str(pair[-1, 0]) + "\n")
    for i in range(len(pair)):   
      if(pair[i, 1] >= 0.0):
        fh.write(" ")
      fh.write("{0:.6e}".format(pair[i, 1]) + " ")
      if(i > 0 and (i+1) % 4 == 0):
        fh.write("\n")
    fh.write("\n")
    fh.write("dens Al ")
    fh.write(str(len(dens)) + " " + str(dens[0, 0]) + " " + str(dens[-1, 0]) + "\n")
    for i in range(len(dens)):   
      if(dens[i, 1] >= 0.0):
        fh.write(" ")
      fh.write("{0:.6e}".format(dens[i, 1]) + " ")
      if(i > 0 and (i+1) % 4 == 0):
        fh.write("\n")
    fh.write("\n")
    fh.write("embe Al ")
    fh.write(str(len(embe)) + " " + str(embe[0, 0]) + " " + str(embe[-1, 0]) + "\n")
    for i in range(len(embe)):   
      if(embe[i, 1] >= 0.0):
        fh.write(" ")
      fh.write("{0:.6e}".format(embe[i, 1]) + " ")
      if(i > 0 and (i+1) % 4 == 0):
        fh.write("\n")
    fh.write("\n")
        


    fh.close()


dlpolyeamfile.run()
