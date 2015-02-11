# -*- coding: utf-8 -*-
"""
Created on Fri Jun 28 12:34:37 2013

@author: nbhushan
"""

import os,sys
dirname=os.path.dirname
sys.path.append(os.path.join(dirname(dirname(__file__)))) 

import numpy as np
from emmissions import Gaussian
from hmm import StandardHMM
import hmmviz as viz
import csv


def test():
    """
    This function has the following workflow:
        1) Define an initial gaussian emmission object
        2) Generate observations from the emmission object
        3) Define intial A , where pi = A[-1]
        4) Train the model and find params which best fit the observations
        5) Visualize the state sequence.
    """
    # adjust the precision of printing float values
    np.set_printoptions( precision=4, suppress=True )    
    
    #Initialize transition Matrix
    A = np.array([[1./5, 1./5, 1./5, 1./5, 1./5], \
                  [1./5, 1./5, 1./5, 1./5, 1./5],\
                  [1./5, 1./5, 1./5, 1./5, 1./5],\
                  [1./5, 1./5, 1./5, 1./5, 1./5], \
                  [1./5, 1./5, 1./5, 1./5, 1./5], \
                  [1./5, 1./5, 1./5, 1./5, 1./5]])   
    # Create an  HMM and Gaussian emmission object        
    emmissionModel = \
        Gaussian(mu = np.array([[3902.85 , 2332.44, 809.70, 258.08, 76.70]]), \
                            covar = np.array([[[341.05]], \
                                              [[215.68]], \
                                              [[189.58]], \
                                              [[90.32]], \
                                              [[47.44]]]))
    typeAmodel = StandardHMM(A, emmissionModel)
    
    #load dauphine110908h19h data, this is a real data set
    
    numseq = 1
    obs = [np.newaxis] * numseq 
    obs[0]= np.loadtxt("dataTypeA.csv",delimiter=",",skiprows=1)[np.newaxis,:]
    #print 'Length of observation sequence 2 :', obs[1].shape[1]
    

    
    print 'Initial Model \n',typeAmodel
    print 'Initial Emission Model\n', typeAmodel.O
    print 'Learning HMM model...'
    
    likelihood,ll, durationlist, ranknlist, reslist= typeAmodel.hmmFit(obs,100,1e-6, debug=False)   
    path=[None]*numseq
    for seq in xrange(numseq):
        path[seq] = typeAmodel.viterbi(obs[seq]) 
    
    print 'LLH: ', likelihood
    print 'Re-estimated Model\n',typeAmodel
    print 'Re-estimated Emission Model\n',typeAmodel.O
    
    
    print "Creating 138 energy profiles of type A"
    profile_list =[]
    n = 0
    while n < 50:
        profile_list.append(typeAmodel.sample(N = 1152)[0][0])
        n = n+1
    new_list = map(list, zip(*profile_list))     
    
    
    with open("HMM_profiles_feederA.csv", "wb") as f:
        writer = csv.writer(f, delimiter = ',')
        writer.writerows(new_list)
        
    #np.savetxt("winter_test_1.csv", X= np.c_[profile_list], delimiter = ',')
        
 #Viterbi state duration
    lengths=[None]*numseq
    for idx,stateseq in enumerate(path):
        lengths[idx] = typeAmodel.estimateviterbiduration(stateseq)
    for length in lengths:   
        for n in range(A.shape[1]):
            print 'Viterbi state duration:', np.max(length[n])

    
    #Visualize
    #filepath = 'C:\\Local\\FINALEXPERIMENTS\\'
    uniqueid = 'feederA_hmm'    
    from matplotlib.pyplot import figure, show   
    from matplotlib.backends.backend_pdf import PdfPages    
    #pp = PdfPages(filepath+uniqueid+'.pdf')      
    pp = PdfPages(uniqueid+'.pdf')
    fa = figure()
    viz.view_viterbi(fa.add_subplot(1,1,1), obs, path, typeAmodel.O.mu, seq=0)   
    fa.tight_layout()  
    pp.savefig()
    '''
    fb=figure()
    viz.view_postduration(fb.add_subplot(111), obs, path, typeAmodel.O.mu, reslist, ranknlist, seq=0)
    fb.tight_layout()
    pp.savefig()
    '''
    fc=figure()
    viz.view_EMconvergence(fc.add_subplot(1,1,1),ll)    
    pp.savefig()
    pp.close()    
    print 'Close the plot window to end the program.'    
    show()         
    
       
 
if __name__ == '__main__':
    test()