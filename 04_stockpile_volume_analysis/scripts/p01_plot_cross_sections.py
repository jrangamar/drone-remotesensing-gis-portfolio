from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_profile(
    profile_data: pd.DataFrame,
    profile_id: str,
    output_path: Path,
    title: str,
) -> None:
    profile = (
        profile_data.loc[profile_data["profile_id"] == profile_id]
        .sort_values("distance")
        .copy()
    )

    if profile.empty:
        raise ValueError(f"No rows found for profile: {profile_id}")

    valid = (
        profile["height_1"].notna()
        & profile["dsm_1"].notna()
        & profile["floor_1"].notna()
    )

    fig, ax = plt.subplots(figsize=(9, 5))

    ax.plot(
        profile["distance"],
        profile["dsm_1"],
        label="Observed DSM surface",
        linewidth=2,
    )
    ax.plot(
        profile["distance"],
        profile["floor_1"],
        label="Estimated bay floor",
        linewidth=2,
    )

    ax.fill_between(
        profile.loc[valid, "distance"],
        profile.loc[valid, "floor_1"],
        profile.loc[valid, "dsm_1"],
        alpha=0.25,
        label="Mapped stockpile material",
    )

    ax.set_title(title)
    ax.set_xlabel("Distance along profile (m)")
    ax.set_ylabel("Elevation (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    input_csv = project_root / "data" / "results" / "p01_profile_samples.csv"
    exports_dir = project_root / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)

    if not input_csv.exists():
        raise FileNotFoundError(f"CSV not found: {input_csv}")

    df = pd.read_csv(input_csv)

    required = {"profile_id", "distance", "dsm_1", "floor_1", "height_1"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    plot_profile(
        df,
        "P01_LONG",
        exports_dir / "profile_longitudinal.png",
        "Section A-A' Longitudinal",
    )

    plot_profile(
        df,
        "P01_CROSS",
        exports_dir / "profile_transverse.png",
        "Section B-B' Transverse",
    )

    print("Created:")
    print(exports_dir / "profile_longitudinal.png")
    print(exports_dir / "profile_transverse.png")


if __name__ == "__main__":
    main()