import pandas as pd
import json
import numpy as np
import scipy.signal
import os

def pipeline(filepath_data, filepath_parameters):
    # Validate file paths
    if not os.path.exists(filepath_data):
        raise FileNotFoundError(f"Data file not found: {filepath_data}")
    if not os.path.exists(filepath_parameters):
        raise FileNotFoundError(f"Parameters file not found: {filepath_parameters}")

    # Load data and parameters
    data = pd.read_csv(filepath_data)
    with open(filepath_parameters, 'r') as f:
        parameters = json.load(f)

    # Validate parameters
    if 'sample_rate' not in parameters or 'threshold' not in parameters:
        raise ValueError("Missing required parameters in the parameters file.")
    if parameters['sample_rate'] <= 0:
        raise ValueError("Sample rate must be positive.")
    if not isinstance(parameters['threshold'], (float, int)):
        raise ValueError("Threshold must be a number.")

    # Validate data
    required_columns = ['trial_on', 'reward_on', 'light_on']
    if not all(column in data.columns for column in required_columns):
        raise ValueError("Data file is missing required columns.")
    if data[required_columns].isna().any().any():
        raise ValueError("Data contains NaNs in critical columns.")

    # Process data
    data = pd.read_csv(filepath_data)
    with open(filepath_parameters, 'r') as f:
        parameters = json.load(f)

    keys_trial = ['trial_on', 'reward_on', 'light_on']
    t, r, l = (data[key] for key in keys_trial)
    keys_neurons = [key for key in data.keys() if key not in keys_trial]
    st = [count_spikes(data[key]) for key in keys_neurons] # 'spike_times'
    st_cat = np.concatenate(st)

    bool_to_idx = lambda x: np.where(x)[0]
    idx_conditions = {
        't': bool_to_idx(t), ## trial_on
        'r': bool_to_idx(r), ## reward_on
        'l': bool_to_idx(l), ## light_on
        'tr': bool_to_idx(t * r),
        'tl': bool_to_idx(t * l),
        'rl': bool_to_idx(r * l),
        'trl': bool_to_idx(t * r * l),
    }    

    ns_conditions = {key: np.isin(st_cat, val).sum() for key, val in idx_conditions.items()}
    return ns_conditions
    

def count_spikes(trace, sample_rate=10000, threshold=10):
    ## smooth the trace
    w = sample_rate / 500 # roughly the n_samples of a spike
    w = int(w + np.remainder(w, 2)) # make odd
    trace_smooth = scipy.signal.savgol_filter(
        x=trace,
        window_length=w, 
        polyorder=2,
    )

    ## find peaks (spike times)
    peaks, _ = scipy.signal.find_peaks(
        x=trace_smooth,
        height=threshold,
        distance=(2/1000 * sample_rate),
    )
    
    return peaks

