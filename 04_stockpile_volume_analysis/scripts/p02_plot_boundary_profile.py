from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_CSV = PROJECT_ROOT / "data/results/p02_boundary_samples_dsm.csv"
OUTPUT_PNG = PROJECT_ROOT / "exports/p02_boundary_elevation_profile.png"


def main() -> None:
    df = pd.read_csv(INPUT_CSV)

    required = {"distance", "dsm_1"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    df = df.sort_values("distance").copy()

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        df["distance"],
        df["dsm_1"],
        linewidth=1.6,
        label="Sampled perimeter elevation",
    )

    ax.set_title("P02 Boundary Elevation Profile")
    ax.set_xlabel("Distance around perimeter (m)")
    ax.set_ylabel("DSM elevation (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(OUTPUT_PNG, dpi=200)
    plt.close(fig)

    print(f"Rows: {len(df)}")
    print(f"Minimum elevation: {df['dsm_1'].min():.3f} m")
    print(f"Maximum elevation: {df['dsm_1'].max():.3f} m")
    print(f"Elevation range: {df['dsm_1'].max() - df['dsm_1'].min():.3f} m")
    print(f"Saved: {OUTPUT_PNG}")


if __name__ == "__main__":
    main()