#import ROOT
#from ROOT import TFile, gROOT
import numpy as np

class RunLocations:
    list_location = 'path/to/your/list_location.txt'
    def get_file_path(self, run_number):
        return [f"mock_path_to_file/Run{run_number}.root"]

run_locations = RunLocations()

def process_runs(training_run_list_str, test_run_list_str):
    # Convert the string of runs entered in the web app to a list
    training_run_list = training_run_list_str.split(',')
    test_run_list = test_run_list_str.split(',')
    # Remove any leading or trailing spaces from each run
    training_run_list = [run.strip() for run in training_run_list]
    test_run_list = [run.strip() for run in test_run_list]
    return training_run_list, test_run_list

    # Lists contain PhiVSEta bins for each run 
    training_runs = []
    test_runs = []
    training_lists = []
    test_lists = []
    norm_list_phieta_train = []
    norm_list_phieta_test = []

#    with open(run_locations.list_location, "r") as file:
#        for line in file:
#            run_number = line.strip()[14:20]
#            filelocation_22 = run_locations.get_file_path(run_number)
#            filelocation_2 = filelocation_22[0]
#            run_num2 = run_number

#            if run_num2 in training_run_list:
#                file = TFile.Open(filelocation_2, "READ")
#                training_runs.append(run_num2)
#                file.cd(f"DQMData/Run {run_num2}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
#                phi_eta = gROOT.FindObject("PhiVSEta")
#                phi_eta_entr = phi_eta.GetEntries()
#                lists_phieta_train = []
#                max_bin_cont = 0.

#                for i in range(53, 1300):
#                    j = i - 52
#                    k = i - 51
#                    if (k % 52 != 0) and (j % 52 != 0):
#                        bin_cont_phieta = phi_eta.GetBinContent(i)
#                        if bin_cont_phieta > max_bin_cont:
#                            max_bin_cont = bin_cont_phieta
#                        b_phieta = bin_cont_phieta / phi_eta_entr
#                        lists_phieta_train.append(b_phieta)
                
#                training_lists.append(lists_phieta_train)
#                b_phieta_norm = max_bin_cont / phi_eta_entr
#                norm_list_phieta_train.append(b_phieta_norm)

  #          if run_num2 in test_run_list:
  #              file = TFile.Open(filelocation_2, "READ")
  #              test_runs.append(run_num2)
  #              file.cd(f"DQMData/Run {run_num2}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
  #              phi_eta = gROOT.FindObject("PhiVSEta")
  #              phi_eta_entr = phi_eta.GetEntries()
  #              lists_phieta_test = []
  #              max_bin_cont = 0.

   #             for i in range(53, 1300):
   #                 j = i - 52
   #                 k = i - 51
   #                 if (k % 52 != 0) and (j % 52 != 0):
   #                     bin_cont_phieta = phi_eta.GetBinContent(i)
   #                     if bin_cont_phieta > max_bin_cont:
   #                         max_bin_cont = bin_cont_phieta
   #                     b_phieta = bin_cont_phieta / phi_eta_entr
   #                     lists_phieta_test.append(b_phieta)

      #          test_lists.append(lists_phieta_test)
     #           b_phieta_norm = max_bin_cont / phi_eta_entr
     #           norm_list_phieta_test.append(b_phieta_norm)

#    return training_runs, test_runs, training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test

#if __name__ == "__main__":
#    import sys
#    training_run_list_str = sys.argv[1]
#    test_run_list_str = sys.argv[2]
#    training_runs, test_runs, training_lists, test_lists, norm_list_phieta_train, norm_list_phieta_test = process_runs(training_run_list_str, test_run_list_str)

    #max_train = max(norm_list_phieta_train) if norm_list_phieta_train else 1
    #max_test = max(norm_list_phieta_test) if norm_list_phieta_test else 1

    #training_list = np.array(training_lists)
    #test_list = np.array(test_lists)
    #training_list = training_list / max_train

