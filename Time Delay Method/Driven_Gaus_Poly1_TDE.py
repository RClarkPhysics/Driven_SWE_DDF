#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 15:34:54 2021

@author: randallclark
"""


import numpy as np
from sklearn.cluster import KMeans


class Gaus_Poly1_TDE:    
    """
    First Make centers for your Training. It useful to do this step seperately as it can take a while to perform for large data sets,
    and if the user wants to perform multiple trainings to select good hyper parameters, it would be unnecessary to recalculate centers
    every time
    inputs:
        Xdata - 1 Dimensional Data that will be used for K-means clustering.
        P - number of centers you want
        D - The number of dimensions you want
        tau - the time delay you want
    """
    def KmeanCenter(self,Xdata,P,D,length,copy,tau):
        #Data should be input as T by D
        XTau = np.zeros((int(D*copy),length))
        for d in range(copy):
            XTau[D*copy-(d+1)*D:D*copy-d*D] = Xdata[0:D,tau*d:length+tau*d]
        centers = KMeans(n_clusters=P, random_state=0).fit(XTau.T).cluster_centers_
        return centers
    
    """
    This is how Data Driven Forecasting is performed when using a Gaussian+Polynomial function representation. The Gaussian form is
    e^[(-||X(n)-C(q)||^2)*R]
    inputs:
        Xdata - the data to be used for training and centers
        length - amount of time to train for
        C - My Centers
        beta - regularization term
        R - parameter used in the Radial basis Fucntion
        D - Dimension of th system being trained on
        copy - The numer of Time Delay Dimensions you have
        tau - the number of time steps inbetween each time delayed dimension
        Forcing - Your Time by Dimension Forcing term values
        h - the length of the time step of your forcing term
    """
    def FuncApproxF(self,Xdata,length,C,beta,R,D,copy,tau,Forcing,h):
        #To Create the F(x) we will need only X to generate Y, then give both to the Func Approxer
        #Xdata will need to be 1 point longer than length to make Y
        #Make sure both X and Y are in D by T format
        Dc = int(D*copy)
        self.Dc = Dc
        self.D = D
        self.tau = tau
        self.copy = copy
        
        #Create the Time Delayed Data From the orignal Data
        XTau = np.zeros((int(D*copy),length+1))
        for d in range(copy):
            XTau[D*copy-(d+1)*D:Dc-d*D] = Xdata[0:D,tau*d:length+1+tau*d]
        
        #Generate Y Target (and do some other simple operations)
        XtauT = XTau.T
        Ydata = self.GenY(XTau[0:D],length,D,Forcing.T,h)
        NcLength = len(C)
        
        #Creat the Phi matrix with those centers
        PhiMat = self.CreatePhiMat(XtauT,C,length,NcLength,R,Dc,D)
        
        #Perform RidgeRegression
        YPhi = np.zeros((D,NcLength+D))
        for d in range(D):
            YPhi[d] = np.matmul(Ydata[d],PhiMat.T)
        PhiPhi = np.linalg.inv(np.matmul(PhiMat,PhiMat.T)+beta*np.identity(NcLength+D))
        W = np.zeros((D,NcLength+D)) 
        for d in range(D):
            W[d] = np.matmul(YPhi[d],PhiPhi)
            
        #Now we want to put together a function to return
        def newfunc(x):
            f = np.matmul(W[0:D,0:NcLength],np.exp(-(np.linalg.norm((x-C),axis=1)**2)*R))
            f = f + np.matmul(W[0:D,NcLength:D+NcLength],x[0:D])
            return f
        
        self.FinalX = XtauT[length-1]
        self.W = W
        return newfunc
        
    """
    Predict ahead in time using the F(t)=dx/dt we just built
    input:
        F - This is the function created above, simply take the above functions output and put it into this input
        PreLength - choose how long you want to predict for
        PData - Choose where to start the prediction, the standard is to pick when the training period ends, but you can choose it
                    to be anywhere. Note that the first tau*(copy-1) values will be used for initiation
        Forcing - Your Time by Dimension Forcing term values
        h - the length of the time step of your forcing term
    """
    def PredictIntoTheFuture(self,F,PreLength,PData,Forcing,h):
        #PData must go from time 0 to tau*(D) and be D dimensional (D by (tau-1)*D)
        def makePre(D,Dc,FinalX,tau,copy):
            #Form the Base
            Prediction = np.zeros((PreLength+tau*(copy-1)+1,D))
            Prediction[0:tau*(copy-1)+1] = PData[0:tau*(copy-1)+1]
    
            #Start by Forming the Bases
            Input = np.concatenate(np.flip(Prediction[0:tau*copy:tau],axis=0))
            Prediction[tau*(copy-1)+1] = Prediction[tau*(copy-1)]+F(Input) + (Forcing[tau*(copy-1)+1]+Forcing[tau*(copy-1)])*h/2
            
            #Let it run forever now
            for t in range(1,PreLength):
                Input = np.concatenate(np.flip(Prediction[t:t+tau*copy:tau],axis=0))
                Prediction[t+tau*(copy-1)+1] = Prediction[t+tau*(copy-1)]+F(Input) + (Forcing[t+tau*(copy-1)+1]+Forcing[t+tau*(copy-1)])*h/2
            return Prediction
        
        Prediction = makePre(self.D,self.Dc,PData,self.tau,self.copy)
        return Prediction.T
    
    """
    These are secondary Functions used in the top function. You need not pay attention to these unless you wish to understand or alter
    the code.
    """     
    
    def CreatePhiMat(self,X,C,Nlength,NcLength,R,D,D0):
        Mat = np.zeros((NcLength + D0,Nlength),dtype = 'float64')
        for i in range(NcLength):
            CC = np.zeros((Nlength,D))
            CC[:] =  C[i]
            Diff = X[0:Nlength]-CC
            Norm = np.linalg.norm(Diff,axis=1)
            Mat[i] = Norm
        Mat[0:NcLength][0:Nlength] = np.exp(-(Mat[0:NcLength][0:Nlength]**2)*R)
        Mat[NcLength:NcLength + D0][0:Nlength] = X.T[0:D0,0:Nlength]
        return Mat

    def GenY(self,Xdata,length,D,Forcing,h):
        #This code is self explanatory. Take the difference
        Y = np.zeros((D,length))
        for d in range(D):
            Y[d] = Xdata[d][1:length+1]-Xdata[d][0:length]-(Forcing[d][0:length]+Forcing[d][1:length+1])*h/2
        return Y
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    