import ROOT
from ROOT import TFile, gROOT
import numpy as np
#import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import subprocess
from ROOT import TCanvas, TProfile, TNtuple, TH1D, TH2D, TH1F, TColor, gROOT, gPad, TText, TFile
from ROOT import gROOT, gBenchmark, gRandom, gSystem, gStyle
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, auc, roc_auc_score
from ROOT import TCanvas, TFile, TProfile, TNtuple, TH1F, TH2F, TLegend, TLine, TGraph, TLatex
from sklearn.neural_network import MLPRegressor
import run_locations

def process_runs(training_run_list_str, test_run_list_str):
    # Convert the string of runs entered in the web app to a list
    training_run_list = training_run_list_str.split(',')
    test_run_list = test_run_list_str.split(',')
    # Remove any leading or trailing spaces from each run
    training_run_list = [run.strip() for run in training_run_list]
    test_run_list = [run.strip() for run in test_run_list]
    return training_run_list, test_run_list

def load_data(training_run_list, test_run_list):
    training_runs = []
    test_runs = []
    training_lists = []
    test_lists = []
    norm_list_phieta_train = []
    norm_list_phieta_test = []
    txt_file = run_locations.make_txt()
    print("--------txt file ----------: ", txt_file)

    with open(txt_file, "w") as file:
        for line in file:
            run_number = line.strip()[14:20]
            filelocation_2 = run_locations.get_file_path(run_number)[0]

            if run_number in training_run_list:
                file = TFile.Open(filelocation_2, "READ")
                training_runs.append(run_number)
                file.cd(f"DQMData/Run {run_number}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
                phi_eta = gROOT.FindObject("PhiVSEta")
                phi_eta_entr = phi_eta.GetEntries()
                lists_phieta_train = []
                max_bin_cont = 0.

                for i in range(53, 1300):
                    j = i - 52
                    k = i - 51
                    if (k % 52 != 0) and (j % 52 != 0):
                        bin_cont_phieta = phi_eta.GetBinContent(i)
                        if bin_cont_phieta > max_bin_cont:
                            max_bin_cont = bin_cont_phieta
                        b_phieta = bin_cont_phieta / phi_eta_entr
                        lists_phieta_train.append(b_phieta)

                training_lists.append(lists_phieta_train)
                b_phieta_norm = max_bin_cont / phi_eta_entr
                norm_list_phieta_train.append(b_phieta_norm)

            if run_number in test_run_list:
                file = TFile.Open(filelocation_2, "READ")
                test_runs.append(run_number)
                file.cd(f"DQMData/Run {run_number}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
                phi_eta = gROOT.FindObject("PhiVSEta")
                phi_eta_entr = phi_eta.GetEntries()
                lists_phieta_test = []
                max_bin_cont = 0.

                for i in range(53, 1300):
                    j = i - 52
                    k = i - 51
                    if (k % 52 != 0) and (j % 52 != 0):
                        bin_cont_phieta = phi_eta.GetBinContent(i)
                        if bin_cont_phieta > max_bin_cont:
                            max_bin_cont = bin_cont_phieta
                        b_phieta = bin_cont_phieta / phi_eta_entr
                        lists_phieta_test.append(b_phieta)

                test_lists.append(lists_phieta_test)
                b_phieta_norm = max_bin_cont / phi_eta_entr
                norm_list_phieta_test.append(b_phieta_norm)

    return training_runs, test_runs, training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test

def normalize_data(training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test):
    max_train = max(norm_list_phieta_train)
    max_test = max(norm_list_phieta_test)
    training_list = np.array(training_lists)
    test_list = np.array(test_lists)
    training_list = training_list / max_train
    test_list = test_list / max_test
    return training_list, test_list

def train_autoencoder(training_list):
    reg = MLPRegressor(hidden_layer_sizes=(1024, 512, 256, 128, 64, 2, 64, 128, 256, 512, 1024),
                       activation='tanh', solver='adam', learning_rate_init=0.001, max_iter=100, tol=0.0001)
    reg.fit(training_list, training_list)
    return reg

def generate_loss_maps(reg, training_list, test_list, output_folder, training_runs, test_runs):
    os.makedirs(output_folder, exist_ok=True)

    x_pred_train = reg.predict(training_list)
    loss_map_train = (training_list - x_pred_train) ** 2
    x_pred_test = reg.predict(test_list)
    loss_map_test = (test_list - x_pred_test) ** 2

    for idx in range(len(training_list)):
        hist_name_tr3 = f"hist_phieta_tr3_{idx}"
        canv_name_tr3 = f"c_phieta_tr3_{idx}"
        hist_phieta_tr3 = TH2F(hist_name_tr3, hist_name_tr3, 50, -5, 5, 24, -3, 3)
        for i in range(24):
            phi = -3.125 + (0.25 * (i + 1))
            for j in range(50):
                eta = -5.1 + (0.2 * (j + 1))
                hist_phieta_tr3.Fill(eta, phi, loss_map_train[idx][i * 50 + j])
        c_phieta_tr3 = TCanvas(canv_name_tr3, canv_name_tr3, 200, 10, 700, 500)
        hist_phieta_tr3.SetTitle(f"Training Run {training_runs[idx]} (Loss Map) ; #eta ; #phi ")
        gStyle.SetPalette(55)
        c_phieta_tr3.Draw()
        hist_phieta_tr3.Draw("colz")
        hist_phieta_tr3.SetStats(0)
        max_z = (np.max(loss_map_train) + (np.max(loss_map_train) / 3))
        hist_phieta_tr3.GetZaxis().SetRangeUser(0, max_z)
        file_name_tr3 = os.path.join(output_folder, f'phieta_train_lossmap_{training_runs[idx]}.png')
        c_phieta_tr3.SaveAs(file_name_tr3)

    for idx in range(len(test_list)):
        hist_name_te3 = f"hist_phieta_te3_{idx}"
        canv_name_te3 = f"c_phieta_te3_{idx}"
        hist_phieta_te3 = TH2F(hist_name_te3, hist_name_te3, 50, -5, 5, 24, -3, 3)
        for i in range(24):
            phi = -3.125 + (0.25 * (i + 1))
            for j in range(50):
                eta = -5.1 + (0.2 * (j + 1))
                hist_phieta_te3.Fill(eta, phi, loss_map_test[idx][i * 50 + j])
        c_phieta_te3 = TCanvas(canv_name_te3, canv_name_te3, 200, 10, 700, 500)
        hist_phieta_te3.SetTitle(f"Test Run {test_runs[idx]} (Loss Map) ; #eta ; #phi ")
        gStyle.SetPalette(55)
        c_phieta_te3.Draw()
        hist_phieta_te3.Draw("colz")
        hist_phieta_te3.SetStats(0)
        max_z = (np.max(loss_map_train) + (np.max(loss_map_train) / 3))
        hist_phieta_te3.GetZaxis().SetRangeUser(0, max_z)
        file_name_te3 = os.path.join(output_folder, f'phieta_test_lossmap_{test_runs[idx]}.png')
        c_phieta_te3.SaveAs(file_name_te3)

def run_analysis(training_run_list_str, test_run_list_str):
    training_run_list, test_run_list = process_runs(training_run_list_str, test_run_list_str)
    training_runs, test_runs, training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test = load_data(training_run_list, test_run_list)
    training_list, test_list = normalize_data(training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test)
    reg = train_autoencoder(training_list)
    generate_loss_maps(reg, training_list, test_list, 'static/', training_runs, test_runs)
