import os
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


def run_predictive_maintenance():
    """Train a Random Forest model and generate predictive maintenance reports."""

    dataset_path = "../data/machine_sensors.csv"

    # Validate input dataset
    if not os.path.exists(dataset_path):
        print(f"Error: '{dataset_path}' not found.")
        return

    # Load dataset
    df = pd.read_csv(dataset_path)

    # Define features and target variable
    feature_columns = [
        "Operating_Hours",
        "Engine_Temperature",
        "Oil_Pressure",
        "Vibration",
        "Machine_Age",
    ]

    X = df[feature_columns]
    y = df["Failure"]

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
    )

    # Train model
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
    )

    model.fit(X_train, y_train)

    # Evaluate model
    predictions = model.predict(X_test)
    classification_report_text = classification_report(y_test, predictions)

    # Calculate feature importance
    feature_importance = pd.DataFrame(
        {
            "Feature": feature_columns,
            "Importance": model.feature_importances_,
        }
    ).sort_values(by="Importance", ascending=False)

    # Predict failures
    df["Failure_Prediction"] = model.predict(X)

    high_risk_machines = df[df["Failure_Prediction"] == 1]

    # Rename columns for Power BI compatibility
    export_df = high_risk_machines.rename(
        columns={
            "Machine_ID": "ID_Maquina",
            "Machine_Type": "Tipo",
            "Operating_Hours": "Horas_Uso",
            "Engine_Temperature": "Temperatura_Motor",
            "Oil_Pressure": "Presion_Aceite",
            "Vibration": "Vibracion",
            "Machine_Age": "Antiguedad_Anios",
            "Failure": "Falla",
            "Failure_Prediction": "Prediccion_Falla",
        }
    )

    # Export results
    output_folder = "../results"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    excel_path = os.path.join(output_folder, "machines_at_risk.xlsx")
    export_df.to_excel(excel_path, index=False)

    report_path = os.path.join(output_folder, "model_summary.txt")

    with open(report_path, "w") as file:

        file.write("====================================================\n")
        file.write("PREDICTIVE MAINTENANCE REPORT\n")
        file.write("====================================================\n\n")

        file.write(f"Total machines analyzed: {len(df)}\n")
        file.write(f"Machines predicted at risk: {len(high_risk_machines)}\n\n")

        file.write("FEATURE IMPORTANCE RANKING\n")
        file.write("----------------------------------------------------\n")

        for _, row in feature_importance.iterrows():
            file.write(f"- {row['Feature']}: {row['Importance'] * 100:.2f}%\n")

        file.write("\nMODEL PERFORMANCE\n")
        file.write("----------------------------------------------------\n")
        file.write(classification_report_text)
        file.write("\n====================================================")

    print(f"Excel report saved to: {excel_path}")
    print(f"Technical report saved to: {report_path}")


if __name__ == "__main__":
    print("Running predictive maintenance analysis...")
    run_predictive_maintenance()