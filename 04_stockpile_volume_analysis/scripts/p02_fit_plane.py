

from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_CSV = PROJECT_ROOT / "data/results/p02_tin_control_points.csv"
FIT_OUTPUT_CSV = PROJECT_ROOT / "data/results/p02_plane_fit.csv"
EQUATION_OUTPUT_TXT = PROJECT_ROOT / "data/results/p02_plane_equation.txt"

X_FIELD = "X"
Y_FIELD = "Y"
Z_FIELD = "dsm_1"


def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Input CSV not found: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    required_fields = {X_FIELD, Y_FIELD, Z_FIELD}
    missing_fields = required_fields.difference(df.columns)
    if missing_fields:
        raise ValueError(
            f"Missing required columns: {sorted(missing_fields)}. "
            f"Available columns: {list(df.columns)}"
        )

    fit_df = df.dropna(subset=[X_FIELD, Y_FIELD, Z_FIELD]).copy()

    if len(fit_df) < 3:
        raise ValueError("At least three valid control points are required.")

    x = fit_df[X_FIELD].to_numpy(dtype=float)
    y = fit_df[Y_FIELD].to_numpy(dtype=float)
    z = fit_df[Z_FIELD].to_numpy(dtype=float)

    design_matrix = np.column_stack([x, y, np.ones_like(x)])
    coefficients, residuals, rank, singular_values = np.linalg.lstsq(
        design_matrix,
        z,
        rcond=None,
    )

    a, b, c = coefficients
    predicted = design_matrix @ coefficients
    residual = z - predicted

    rmse = float(np.sqrt(np.mean(residual**2)))
    mae = float(np.mean(np.abs(residual)))
    residual_min = float(np.min(residual))
    residual_max = float(np.max(residual))

    fit_df["plane_predicted_m"] = predicted
    fit_df["plane_residual_m"] = residual
    fit_df.to_csv(FIT_OUTPUT_CSV, index=False)

    equation_text = (
        "P02 least-squares plane fitted to cleaned perimeter controls\n"
        f"z = ({a:.12f} * x) + ({b:.12f} * y) + ({c:.12f})\n"
        f"control_points = {len(fit_df)}\n"
        f"rank = {rank}\n"
        f"rmse_m = {rmse:.6f}\n"
        f"mae_m = {mae:.6f}\n"
        f"residual_min_m = {residual_min:.6f}\n"
        f"residual_max_m = {residual_max:.6f}\n"
    )
    EQUATION_OUTPUT_TXT.write_text(equation_text, encoding="utf-8")

    print(f"Control points used: {len(fit_df)}")
    print(
        "Plane equation: "
        f"z = ({a:.12f} * x) + ({b:.12f} * y) + ({c:.12f})"
    )
    print(f"RMSE: {rmse:.6f} m")
    print(f"MAE: {mae:.6f} m")
    print(f"Residual minimum: {residual_min:.6f} m")
    print(f"Residual maximum: {residual_max:.6f} m")
    print(f"Saved: {FIT_OUTPUT_CSV}")
    print(f"Saved: {EQUATION_OUTPUT_TXT}")


if __name__ == "__main__":
    main()