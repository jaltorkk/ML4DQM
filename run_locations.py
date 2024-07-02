import os
import sys
import ast

def process_runs(training_run_list_str, test_run_list_str):
    # Convert the string of runs entered in the web app to a list
    training_run_list = training_run_list_str.split(',')
    test_run_list = test_run_list_str.split(',')
    # Remove any leading or trailing spaces from each run
    training_run_list = [run.strip() for run in training_run_list]
    test_run_list = [run.strip() for run in test_run_list]
    return training_run_list, test_run_list

# Run-3 2023 file path
def get_file_path(run_number):
    original_path_1 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/JetMET1/" # this is the locatrion where all runs are
    original_path_2 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/JetMET/"
    count = 0
    run_no=int(run_number)
    while run_no != 0:
        run_no //= 10
        count += 1
    file_prefix = run_number[:(count-2)].zfill(7)
    file_path_1 = os.path.join(original_path_1, file_prefix+"xx") # this to insert the run number to the original location
    file_path_2 = os.path.join(original_path_2, file_prefix+"xx")

    if os.path.exists(file_path_1):
        list_location_all_1 = os.listdir(file_path_1)
        list_location_1 = [file for file in list_location_all_1 if file.endswith('.root')]
        for file_name_1 in list_location_1:
            if run_number in file_name_1:
                file_path_1 = [os.path.join(file_path_1, file_name_1)]
                return file_path_1
    elif os.path.exists(file_path_2):
        list_location_all_2 = os.listdir(file_path_2)
        list_location_2 = [file for file in list_location_all_2 if file.endswith('.root')]
        for file_name_2 in list_location_2:
            if run_number in file_name_2:
                file_path_2 = [os.path.join(file_path_2, file_name_2)]
                return file_path_2
    print(f"This run {run_number} does not exist for JetMET PD.")
    return None

def make_txt():
    # Parse command-line arguments
    training_run_list, test_run_list = process_runs()

    # File location
    filelocation = " "
    list_location = " "
    if len(trainingrunlist) == 0:
        filelocation = "/eos/user/i/iatakisi/Depo/DQM_DC/2018PromptReco/"
        list_location = "runlist_2018.txt"
        with open(list_location, 'w') as file:
            files = os.listdir(filelocation)
            for f in files:
                if "DQM_" in f:
                    file.write(f"{f}\n")
    else:
        for run_number in trainingrunlist + testrunlist:
            file_paths = get_file_path(run_number)
            if file_paths:
                filelocation = file_paths[0][:file_paths[0].rfind('/') + 1]
                list_loc = os.path.basename(file_paths[0])
                with open("runlist_2023.txt", 'a') as file:
                    file.write(f'{list_loc}\n')
                list_location = "runlist_2023.txt"
    print("--------------------------------------------list location :-------------------------------- ",list_location)
    return list_location
                
#if __name__ == "__main__":
#    main()


# Default Example: Prompt-Reco 2018 Runs Era A (Train) and Era D (Test).
training_runs_2d_2018=['315267', '315270', '315322', '315339', '315357', '315361', '315363', '315366', '315420', '315489', 
                       '315506', '315510', '315543', '315555', '315556', '315557', '315640', '315642', '315644', '315645', 
                       '315646', '315647', '315648', '315689', '315690', '315702', '315703', '315704', '315705', '315713', 
                       '315721', '315741', '315764', '315770', '315785', '315786', '315790', '315801', '315973', '316059', 
                       '316110', '316114', '316186', '316187', '316199', '316200', '316201', '316202', '316216', '316217', 
                       '316239', '316240', '316241', '316271', '316361', '316362', '316363', '316377', '316378', '316379', 
                       '316380', '316455', '316457', '316469', '316470', '316472', '316505', '316569', '316590', '316613', 
                       '316615', '316666', '316667', '316700', '316701', '316702', '316715', '316716', '316717', '316719', 
                       '316720', '316722', '316723', '316758', '316766', '316876', '316877', '316879', '316928', '316985', 
                       '316993', '316995']

test_runs_2d_2018=['320673', '320674', '320688', '320712', '320757', '320804', '320807', '320809', '320821', '320822', 
                   '320823', '320824', '320838', '320840', '320841', '320853', '320854', '320855', '320856', '320857', 
                   '320858', '320859', '320887', '320888', '320916', '320917', '320920', '320933', '320934', '320936', 
                   '320941', '320980', '320995', '320996', '321004', '321005', '321006', '321007', '321009', '321010', 
                   '321011', '321012', '321051', '321055', '321067', '321068', '321069', '321119', '321121', '321122', 
                   '321124', '321126', '321134', '321138', '321140', '321149', '321165', '321166', '321167', '321178', 
                   '321218', '321219', '321221', '321230', '321231', '321232', '321233', '321262', '321283', '321294', 
                   '321305', '321311', '321312', '321313', '321393', '321396', '321397', '321414', '321415', '321431', 
                   '321432', '321433', '321434', '321436', '321457', '321461', '321475', '321710', '321735', '321755', 
                   '321776', '321777', '321813', '321815', '321817', '321818', '321820', '321831', '321832', '321833', 
                   '321834', '321879', '321880', '321887', '321908', '321909', '321917', '321919', '321933', '321960', 
                   '321961', '321973', '321975', '321988', '321990', '322013', '322014', '322022', '322040', '322057', 
                   '322068', '322079', '322106', '322113', '322118', '322179', '322201', '322204', '322222', '322252', 
                   '322317', '322319', '322322', '322324', '322332', '322348', '322355', '322356', '322381', '322407', 
                   '322430', '322431', '322480', '322492', '322510', '322599', '322602', '322603', '322605', '322617', 
                   '322625', '322633', '323414', '323423', '323470', '323471', '323472', '323473', '323474', '323475', 
                   '323487', '323488', '323492', '323493', '323495', '323524', '323525', '323526', '323693', '323696', 
                   '323702', '323725', '323727', '323755', '323775', '323778', '323790', '323794', '323841', '323857', 
                   '323940', '323954', '323976', '323978', '323980', '323983', '323997', '324021', '324022', '324077', 
                   '324201', '324202', '324205', '324206', '324207', '324209', '324237', '324245', '324293', '324315', 
                   '324318', '324420', '324729', '324747', '324764', '324765', '324769', '324772', '324785', '324791', 
                   '324835', '324840', '324841', '324846', '324878', '324897', '324970', '324980', '324997', '324998', 
                   '324999', '325000', '325001', '325022', '325057', '325097', '325098', '325099', '325100', '325101', 
                   '325110', '325117', '325159', '325168', '325169', '325170', '325172']
