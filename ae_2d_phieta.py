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


