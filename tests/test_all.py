import pytest
from my_pipeline.pipeline import pipeline

def test_ill_conditioned_input():
    # Define a path to a non-existent file or a file with missing columns
    filepath_data = 'path/to/nonexistent_or_invalid_file.csv'
    filepath_parameters = 'path/to/parameters.json'

    with pytest.raises(ValueError):
        pipeline(filepath_data, filepath_parameters)


def test_accuracy():
    # Create fake data with known properties
    filepath_data, filepath_parameters = create_fake_data_for_testing()
    
    # Run the pipeline
    result = pipeline(filepath_data, filepath_parameters)

    # Assert that the output matches expected values
    expected_output = {'t': 300, 'r': 150, 'l': 350, 'tr': 140, 'tl': 180, 'rl': 100, 'trl': 100}
    assert result == expected_output, "Pipeline output does not match expected values"


def create_fake_data_for_testing(filepath_data='/path/to/fake_data.csv', 
                                 filepath_parameters='/path/to/fake_parameters.json', 
                                 num_neurons=5, num_samples=10000, 
                                 spike_rate=0.01, noise_level=5):
    """
    Creates fake data and parameters files for testing the pipeline function.

    Args:
        filepath_data (str): Filepath to save the fake data CSV file.
        filepath_parameters (str): Filepath to save the fake parameters JSON file.
        num_neurons (int): Number of neurons to simulate.
        num_samples (int): Number of samples in the voltage traces.
        spike_rate (float): Proportion of samples that should be spikes.
        noise_level (float): Standard deviation of the noise in the voltage trace.
    """
    # Create condition flags
    trial_on = np.random.choice([True, False], num_samples)
    reward_on = np.random.choice([True, False], num_samples)
    light_on = np.random.choice([True, False], num_samples)

    # Create voltage traces
    data = {'trial_on': trial_on, 'reward_on': reward_on, 'light_on': light_on}
    for i in range(num_neurons):
        spikes = np.random.choice([True, False], num_samples, p=[spike_rate, 1-spike_rate])
        noise = np.random.normal(0, noise_level, num_samples)
        voltage_trace = noise + spikes * 100  # Spikes are 100 units above the noise
        data[f'neuron_{i+1}'] = voltage_trace

    # Save data to CSV
    pd.DataFrame(data).to_csv(filepath_data, index=False)

    # Create and save parameters file
    parameters = {
        'sample_rate': 1000,
        'threshold': 50  # Threshold for spike detection
    }
    with open(filepath_parameters, 'w') as file:
        json.dump(parameters, file)

    return filepath_data, filepath_parameters

# Example usage
fake_data_path, fake_params_path = create_fake_data_for_testing('/path/to/fake_data.csv', '/path/to/fake_parameters.json')


