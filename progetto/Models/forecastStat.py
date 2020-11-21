import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import os, sys, io, base64

def print_figure(fig):
	"""
	Converts a figure (as created e.g. with matplotlib or seaborn) to a png image and this 
	png subsequently to a base64-string, then prints the resulting string to the console.
	"""
	buf = io.BytesIO()
	fig.savefig(buf, format='png')
	print(base64.b64encode(buf.getbuffer()))


if __name__ == "__main__":
   # change working directory to script path
   abspath = os.path.abspath(__file__)
   dname = os.path.dirname(abspath)
   os.chdir(dname)

   print('MAPE Number of arguments:', len(sys.argv))
   print('MAPE Argument List:', str(sys.argv) )#, ' first true arg:',sys.argv[1])   #questo va decommentato
   
   dffile = "FTSE_MIB_.csv"#sys.argv[1] #questo va decommentato e passato come argomento
   df = pd.read_csv("../risultati/"+dffile)
   
   plt.plot(df)
   #plt.show()
   
   # Finally, print the chart as base64 string to the console.
   print_figure(plt.gcf())
   