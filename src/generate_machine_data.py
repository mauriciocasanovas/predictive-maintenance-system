import numpy as np
import pandas as pd


def generate_dataset(filename = "../data/machine_sensors.csv"):
    """Generate a synthetic dataset for predictive maintenance."""

    np.random.seed(42)
    num_records = 1000

    data = {
        "Machine_ID": [f"MAQ-{i:04d}" for i in range(1, num_records + 1)],
        "Machine_Type": np.random.choice(["Tractor", "Harvester"], num_records),
        "Operating_Hours": np.random.randint(100, 8000, num_records),
        "Engine_Temperature": np.random.uniform(60, 120, num_records),
        "Oil_Pressure": np.random.uniform(15, 85, num_records),
        "Vibration": np.random.uniform(1, 15, num_records),
        "Machine_Age": np.random.randint(1, 20, num_records),
    }

    df = pd.DataFrame(data)

    # Failure logic based on sensor thresholds
    failure_condition = (
        (df["Engine_Temperature"] > 105)
        | (df["Oil_Pressure"] < 25)
        | (df["Vibration"] > 12)
    )

    df["Failure"] = failure_condition.astype(int)

    df.to_csv(filename, index=False)

    print(f"Dataset '{filename}' generated successfully with {num_records} records.")


if __name__ == "__main__":
    generate_dataset()