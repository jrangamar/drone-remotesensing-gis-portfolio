from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_csv = project_root / "data" / "results" / "p01_floor_sample_centroids.csv"
    output_csv = project_root / "data" / "results" / "p01_floor_plane_fit.csv"
    output_txt = project_root / "data" / "results" / "p01_floor_plane_equation.txt"

    if not input_csv.exists():
        raise FileNotFoundError(f"Input CSV not found: {input_csv}")

    df = pd.read_csv(input_csv)

    required = ["sample_id", "x_coord", "y_coord", "z_mean"]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    x = df["x_coord"].to_numpy(dtype=float)
    y = df["y_coord"].to_numpy(dtype=float)
    z = df["z_mean"].to_numpy(dtype=float)

    design_matrix = np.column_stack([x, y, np.ones(len(df))])
    a, b, c = np.linalg.lstsq(design_matrix, z, rcond=None)[0]

    df["z_pred"] = a * x + b * y + c
    df["residual_m"] = z - df["z_pred"]

    rmse = float(np.sqrt(np.mean(df["residual_m"] ** 2)))

    equation = (
        f"z = ({a:.12f} * x) + ({b:.12f} * y) + ({c:.12f})"
    )

    df.to_csv(output_csv, index=False)

    output_txt.write_text(
        "\n".join(
            [
                "Fitted bay-floor plane",
                equation,
                f"RMSE_m = {rmse:.6f}",
                f"Sample_count = {len(df)}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    print("Plane equation:")
    print(equation)
    print()
    print(
        df[
            ["sample_id", "z_mean", "z_pred", "residual_m"]
        ].to_string(index=False)
    )
    print()
    print(f"RMSE: {rmse:.4f} m")
    print(f"Saved results: {output_csv}")
    print(f"Saved equation: {output_txt}")


if __name__ == "__main__":
    main()