import numpy as np
import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from optparse import OptionParser

parser = OptionParser()
parser.add_option("-i", "--input", dest="input", default='Bias_mu.txt', type="str", help="input file")
(options, args) = parser.parse_args()

def main():
    
    

    for m in range(1,31,1):
        print "[[ Info ]] plot mass point: " + str(m)

        f = open("Bias_M"+str(m)+".txt")
        f_lines = f.readlines()

        if f_lines == []:
            print "[[ Error ]] mass point: " + str(m) + " was empty"
            continue

        bias_test=[]
        bias_name=[]
        bias_true=[]
        exp = f_lines[0].rstrip('\n').rstrip().split('\t')
        exp_name = f_lines[1].rstrip('\n').split('\t')
        for i in range(len(exp)):
            bias_test.append(float(exp[i]))
            bias_name.append(exp_name[i])
        bias_true.append(round(float(f_lines[2].rstrip('\n')),2))
        print bias_test

        x=np.array(bias_test)
        y=0.5*np.ones(len(bias_test))

        plt.xlabel('$\\frac{\mu-\\tilde{\mu}}{\sigma_{\mu}}$',fontsize=30)
        plt.ylabel('$\\tilde{\mu}$',fontsize=20)
        plt.xlim(xmax=0.5,xmin=-0.5)
        plt.ylim(ymax=1.0,ymin=0)

        colors = ['red','orange','blue','purple','darkturquoise','yellow','green','pink','black']
        area = np.pi * 4**2

        plt.plot([0.14, 0.14], [0., 1], c='black', linestyle='--')
        plt.plot([-0.14, -0.14], [0., 1], c='black', linestyle='--')
        plt.yticks(np.array([0.5]),np.array(bias_true))
        for j in range(len(bias_test)):
            plt.scatter(x[j], y[j], s=area, c=colors[j], alpha=0.4, label=bias_name[j])

        #plt.title('Toy Function: 3rd Order Power Low (' +mass[i] + ')')
        plt.grid()
        plt.legend()
        plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.15)
        plt.savefig('./BiasPlot_UL/M'+str(m) + '.png',dpi=300)
        plt.close('all')
        #plt.show()

main()
