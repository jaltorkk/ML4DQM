from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import csv
import os
import sys
import subprocess
import re, codecs
import ROOT
from ROOT import TFile
from ROOT import gROOT
from ROOT import TCanvas, TProfile, TNtuple, TH1D, TH2D, TH1F, TColor, gROOT, gPad, TText
import ctypes
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc
from sklearn.metrics import roc_auc_score
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TLegend, TLine, TGraph, TLatex
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
import tensorflow as tf
from sklearn.neural_network import MLPRegressor
import run_locations

# do cleaning for images
#os.system("rm *.txt images_phieta/*.png images_phieta/*.img images_phieta/*.jpg")
#os.system("rm *images_phieta/*.png images_phieta/*.img images_phieta/*.jpg")

def process_runs(training_run_list_str,test_run_list_str):
    # Convert the string of runs entered in the web app to a list
    training_run_list = training_run_list_str.split(',')
    test_run_list = test_run_list_str.split(',')
    # Remove any leading or trailing spaces from each run
    training_run_list = [run.strip() for run in training_run_list]
    test_run_list = [run.strip() for run in test_run_list]
    # Add double quotes around each run
    training_run_list = ['"' + run + '"' for run in training_run_list]
    test_run_list = ['"' + run + '"' for run in test_run_list]
    # Lists contain PhiVSEta bins for each run 
    training_runs=[]
    test_runs=[]
    training_lists=[]
    test_lists=[]
    norm_list_phieta_train=[]
    norm_list_phieta_test=[]
    with open(run_locations.list_location,"r") as file:
    # reading each line
    for line in file:
        # reading each word
        for word in line.split():
            run_number = word[14:20]
            filelocation_22 = run_locations.get_file_path(run_number)
            filelocation_2 = filelocation_22[0]
            run_num2 = word[14:20]
            if run_num2 in training_run_list:
                file = TFile.Open(filelocation_2, "READ")
                run_num = word[14:20]
                training_runs.append(run_num)
                file.cd("DQMData/Run " + run_num + "/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")   
                phi_eta=gROOT.FindObject("PhiVSEta") 
                file.cd("DQMData/Run "+run_num+"/JetMET/Run summary")
                phi_eta_entr=phi_eta.GetEntries()
                lists_phieta_train=[] 
                max_bin_cont=0.
                for i in range(53,1300):
                    j=i-52
                    k=i-51
                    if (k%52.!=0) and (j%52.!=0):
                        bin_cont_phieta=phi_eta.GetBinContent(i)
                        if (bin_cont_phieta>max_bin_cont):
                            max_bin_cont=bin_cont_phieta
                        b_phieta=(bin_cont_phieta/phi_eta_entr)
                        lists_phieta_train.append(b_phieta)
                training_lists.append(lists_phieta_train)
                b_phieta_norm=max_bin_cont/phi_eta_entr
                norm_list_phieta_train.append(b_phieta_norm)
            if run_num2 in test_run_list:
                file = TFile.Open(filelocation_2, "READ")
                run_num = word[14:20]
                test_runs.append(run_num)
                file.cd("DQMData/Run " + run_num + "/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")   
                phi_eta=gROOT.FindObject("PhiVSEta") 
                file.cd("DQMData/Run "+run_num+"/JetMET/Run summary")
                phi_eta_entr=phi_eta.GetEntries()
                lists_phieta_test=[] 
                max_bin_cont=0.
                for i in range(53,1300):
                    j=i-52
                    k=i-51
                    if (k%52.!=0) and (j%52.!=0):
                        bin_cont_phieta=phi_eta.GetBinContent(i)
                        if (bin_cont_phieta>max_bin_cont):
                            max_bin_cont=bin_cont_phieta
                        b_phieta=(bin_cont_phieta/phi_eta_entr)
                        lists_phieta_test.append(b_phieta)
                test_lists.append(lists_phieta_test)
                b_phieta_norm=max_bin_cont/phi_eta_entr
                norm_list_phieta_test.append(b_phieta_norm)
    return training_runs,test_runs,training_lists,test_lists,norm_list_phieta_train,norm_list_phieta_test

# Normalize training and test runs
max_train=max(norm_list_phieta_train)
max_test=max(norm_list_phieta_test)
training_list=np.array(training_lists)  
test_list=np.array(test_lists)
training_list=training_list/max_train 
test_list=test_list/max_test

n_train1 = training_list.shape[0]
n_test1 = test_list.shape[0]
print ("The number of training images for PhiVSEta : {}, shape : {}".format(n_train1, training_list.shape))
print ("The number of testing images for PhiVSEta : {}, shape : {}".format(n_test1, test_list.shape))
    
#--------------------------Define a Structure of an Autoencoder-----------------------------
# Encoder structure
n_encoder1 = 1024
n_encoder2 = 512
n_encoder3 = 256
n_encoder4 = 128
n_encoder5 = 64
# latent
n_latent = 2
# Decoder structure
n_decoder5 = 64
n_decoder4 = 128
n_decoder3 = 256
n_decoder2 = 512
n_decoder1 = 1024

reg= MLPRegressor(hidden_layer_sizes = (n_encoder1, n_encoder2, n_encoder3, n_encoder4, n_encoder5, n_latent, 
                   n_decoder5, n_decoder4, n_decoder3, n_decoder2, n_decoder1), 
                   activation = 'tanh', 
                   solver = 'adam', 
                   learning_rate_init = 0.001, 
                   max_iter = 100, 
                   tol = 0.0001, 
                   verbose = False)
reg.fit(training_list, training_list)

#------------------------------------- loss maps ------------------------------------------
# --------------------------------- Phi VS Eta----------------------------------------------
# Training runs
x_pred_train = reg.predict(training_list)
x_pred_train = np.array(x_pred_train)
# Reconstructed image
x_reconst_train=[]
for i in range(len(x_pred_train)):
    img = x_pred_train[i].reshape(24,50)
    x_reconst_train.append(img)
# Loss map
loss_map_tr=(training_list-x_pred_train)**2
loss_map_tr=np.array(loss_map_tr)
loss_map_train=[]
for i in range(len(loss_map_tr)):
    img = loss_map_tr[i].reshape(24,50)
    loss_map_train.append(img)

# Test runs
x_pred_test = reg.predict(test_list)
x_pred_test = np.array(x_pred_test)
# Reconstructed image
x_reconst_test=[]
for i in range(len(x_pred_test)):
    img = x_pred_test[i].reshape(24,50)
    x_reconst_test.append(img)
# Loss map
loss_map_te=(test_list-x_pred_test)**2
loss_map_te=np.array(loss_map_te)
loss_map_test=[]
for i in range(len(loss_map_te)):
    img = loss_map_te[i].reshape(24,50)
    loss_map_test.append(img)    
    
# --------------------------------------testing training data for PhiVSEta--------------------------------------
# Reshape the training and test data to 24X50 to draw histogram
img_train=[]
for i in range(len(training_list)):
    img = training_list[i].reshape(24,50)
    img_train.append(img)
        
# ----------------- Orginal histogram -----------------
for idx in range(len(training_runs)):
    hist_phieta_tr1=TH2F("hist_phieta_tr1","hist_phieta_tr1",50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_tr1.Fill(eta,phi,img_train[idx][i][j])
    c_phieta_tr1 = TCanvas( 'c_phieta_tr1', 'c_phieta_tr1', 200, 10, 700, 500)
    hist_phieta_tr1.SetTitle("Training Run " + training_runs[idx] +  " (Original) ; #eta ; #phi ")
    gStyle.SetPalette(55)

# ----------------- Reconstructed histogram -----------------
for idx in range(len(training_runs)):
    hist_phieta_tr2=TH2F("hist_phieta_tr2","hist_phieta_tr2",50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_tr2.Fill(eta,phi,x_reconst_train[idx][i][j])
    c_phieta_tr2 = TCanvas( 'c_phieta_tr2', 'c_phieta_tr2', 200, 10, 700, 500)
    hist_phieta_tr2.SetTitle("Training Run " + training_runs[idx] +  " (Reconstructed) ; #eta ; #phi ")
    gStyle.SetPalette(55)

# ----------------- Loss Map histogram (MSE) -----------------
hist_loss_forall=TH1F("hist_loss_forall","hist_loss_forall",50,0,0.5)
for idx in range(len(training_runs)):
    hist_name_tr3 = f"hist_phieta_tr3_{idx}"
    canv_name_tr3 = f"c_phieta_tr3_{idx}"
    hist_phieta_tr3 = {}
    c_phieta_tr3 = {}
    file_name_tr3 = {}  
    hist_phieta_tr3[idx]=TH2F(hist_name_tr3,hist_name_tr3,50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_tr3[idx].Fill(eta,phi,loss_map_train[idx][i][j])
            hist_loss_forall.Fill(loss_map_train[idx][i][j])
    c_phieta_tr3[idx] = TCanvas( canv_name_tr3, canv_name_tr3, 200, 10, 700, 500)
    hist_phieta_tr3[idx].SetTitle("Training Run " + training_runs[idx] +  " (Loss Map) ; #eta ; #phi ")
    gStyle.SetPalette(55)
    c_phieta_tr3[idx].Draw()
    hist_phieta_tr3[idx].Draw("colz")
    hist_phieta_tr3[idx].SetStats(0)
    max_z=(np.max(loss_map_train)+(np.max(loss_map_train)/3))
    hist_phieta_tr3[idx].GetZaxis().SetRangeUser(0,max_z)
    file_name_tr3[idx] = f"loss_maps_images/phieta_train_lossmap_{training_runs[idx]}.png"
    c_phieta_tr3[idx].SaveAs(file_name_tr3[idx])   
c_hist_loss_forall = TCanvas( "c_hist_loss_forall", "c_hist_loss_forall", 200, 10, 700, 500)
c_hist_loss_forall.SetLogy()
hist_loss_forall.Draw()
c_hist_loss_forall.SaveAs("loss_maps_images/loss_all.png")
# --------------------------------------testing test data for PhiVSEta--------------------------------------
# Reshape test data to 24X50 to draw histograms
img_test=[]
for i in range(len(test_list)):
    img = test_list[i].reshape(24,50)
    img_test.append(img)
# ----------------- Orginal histogram -----------------
for idx in range(len(test_runs)):
    hist_phieta_te1=TH2F("hist_phieta_te1","hist_phieta_te1",50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_te1.Fill(eta,phi,img_test[idx][i][j])
    c_phieta_te1 = TCanvas( 'c_phieta_te1', 'c_phieta_te1', 200, 10, 700, 500)
    hist_phieta_te1.SetTitle("Test Run " + test_runs[idx] +  " (Original) ; #eta ; #phi ")
    gStyle.SetPalette(55)  

# ----------------- Reconstructed histogram -----------------
for idx in range(len(test_runs)):
    hist_phieta_te2=TH2F("hist_phieta_te2","hist_phieta_te2",50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_te2.Fill(eta,phi,x_reconst_test[idx][i][j])
    c_phieta_te2 = TCanvas( 'c_phieta_te2', 'c_phieta_te2', 200, 10, 700, 500)
    hist_phieta_te2.SetTitle("Test Run " + test_runs[idx] +  " (Reconstructed) ; #eta ; #phi ")
    gStyle.SetPalette(55)               

# ----------------- Loss Map histogram (MSE) -----------------
for idx in range(len(test_runs)):
    hist_name_te3 = f"hist_phieta_te3_{idx}"
    canv_name_te3 = f"c_phieta_te3_{idx}"
    hist_outliers_name_te3 = f"hist_outliers_name_te3_{idx}"
    hist_outliers_te3 = {}
    canv_outliers_name_te3 = f"c_outliers_te3_{idx}"
    c_outliers_te3 = {}
    hist_phieta_te3 = {}
    c_phieta_te3 = {}
    file_name_te3 = {}
    file_name_outliers_te3={}
    hist_outliers_te3[idx]=TH2F(hist_outliers_name_te3,hist_outliers_name_te3,50,-5,5,24,-3,3)
    hist_phieta_te3[idx]=TH2F(hist_name_te3,hist_name_te3,50,-5,5,24,-3,3)
    for i in range(0,24):
        phi=-3.125+(0.25*(i+1))
        for j in range(0,50):
            eta=-5.1+(0.2*(j+1))
            hist_phieta_te3[idx].Fill(eta,phi,loss_map_test[idx][i][j])
            if loss_map_test[idx][i][j]>np.max(loss_map_train):
                hist_outliers_te3[idx].Fill(eta,phi,loss_map_test[idx][i][j])
                
    c_phieta_te3[idx] = TCanvas( canv_name_te3, canv_name_te3, 200, 10, 700, 500)
    hist_phieta_te3[idx].SetTitle("Test Run " + test_runs[idx] +  " (Loss Map) ; #eta ; #phi ")
    gStyle.SetPalette(55)
    c_phieta_te3[idx].Draw()
    hist_phieta_te3[idx].Draw("colz")
    hist_outliers_te3[idx].Draw("box text same")
    hist_phieta_te3[idx].SetStats(0)
    hist_phieta_te3[idx].GetZaxis().SetRangeUser(0,max_z)
    file_name_te3[idx] = f"loss_maps_images/phieta_test_lossmap_{test_runs[idx]}.png"
    c_phieta_te3[idx].SaveAs(file_name_te3[idx])
    c_outliers_te3[idx] = TCanvas( canv_outliers_name_te3, canv_outliers_name_te3, 200, 10, 700, 500)
    hist_outliers_te3[idx].Draw("box")
    file_name_outliers_te3[idx] = f"loss_maps_images/outliers_test_lossmap_{test_runs[idx]}.png"
    c_outliers_te3[idx].SaveAs(file_name_outliers_te3[idx])
