import os
import sys
import ast

# Run-3 2023 file path
def get_file_path(run_number):
    original_path_1 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/JetMET1/" # this is the locatrion where all runs are
    original_path_2 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2023/JetMET/"
    original_path_3 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2024/JetMET0/"
    original_path_4 = "/eos/cms/store/group/comm_dqm/DQMGUI_data/Run2024/JetMET1/"
    count = 0
    run_no=int(run_number)
    while run_no != 0:
        run_no //= 10
        count += 1
    file_prefix = run_number[:(count-2)].zfill(7)
    file_path_1 = os.path.join(original_path_1, file_prefix+"xx") # this to insert the run number to the original location
    file_path_2 = os.path.join(original_path_2, file_prefix+"xx")
    file_path_3 = os.path.join(original_path_3, file_prefix+"xx")
    file_path_4 = os.path.join(original_path_4, file_prefix+"xx")

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
    elif os.path.exists(file_path_3):
        list_location_all_3 = os.listdir(file_path_3)
        list_location_3 = [file for file in list_location_all_3 if file.endswith('.root')]
        for file_name_3 in list_location_3:
            if run_number in file_name_3:
                file_path_3 = [os.path.join(file_path_3, file_name_3)]
                return file_path_3
    elif os.path.exists(file_path_4):
        list_location_all_4 = os.listdir(file_path_4)
        list_location_4 = [file for file in list_location_all_4 if file.endswith('.root')]
        for file_name_4 in list_location_4:
            if run_number in file_name_2:
                file_path_4 = [os.path.join(file_path_4, file_name_4)]
                return file_path_4
    return None
