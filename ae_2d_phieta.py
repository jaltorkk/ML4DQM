import ROOT
from ROOT import TFile, gROOT
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

with open(run_locations.list_location, "r") as file:
    for line in file:
        run_number = line.strip()[14:20]
        filelocation_22 = run_locations.get_file_path(run_number)
        filelocation_2 = filelocation_22[0]
        run_num2 = run_number

        if run_num2 in training_run_list:
            file = TFile.Open(filelocation_2, "READ")
            training_runs.append(run_num2)
            file.cd(f"DQMData/Run {run_num2}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
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

        if run_num2 in test_run_list:
            file = TFile.Open(filelocation_2, "READ")
            test_runs.append(run_num2)
            file.cd(f"DQMData/Run {run_num2}/JetMET/Run summary/Jet/Cleanedak4PFJetsCHS")
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
# Loss map
loss_map_te=(test_list-x_pred_test)**2
loss_map_te=np.array(loss_map_te)
loss_map_test=[]
for i in range(len(loss_map_te)):
    img = loss_map_te[i].reshape(24,50)
    loss_map_test.append(img)    

