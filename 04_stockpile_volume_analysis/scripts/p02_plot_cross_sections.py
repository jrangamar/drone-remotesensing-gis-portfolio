from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]

INPUT_CSV = PROJECT_ROOT / "data/results/p02_profile_samples.csv"
LONGITUDINAL_OUTPUT = PROJECT_ROOT / "exports/p02_profile_longitudinal.png"
TRANSVERSE_OUTPUT = PROJECT_ROOT / "exports/p02_profile_transverse.png"

PROFILE_FIELD = "profile_id"
DISTANCE_FIELD = "distance"
DSM_FIELD = "dsm_1"
BASE_FIELD = "tin_1"
HEIGHT_FIELD = "height_1"


def prepare_profile(df: pd.DataFrame, profile_id: str) -> pd.DataFrame:
    profile = df.loc[df[PROFILE_FIELD] == profile_id].copy()

    if profile.empty:
        raise ValueError(f"No rows found for profile_id={profile_id!r}")

    profile = profile.sort_values(DISTANCE_FIELD)

    for field in [DISTANCE_FIELD, DSM_FIELD, BASE_FIELD, HEIGHT_FIELD]:
        profile[field] = pd.to_numeric(profile[field], errors="coerce")

    return profile


def plot_profile(
    profile: pd.DataFrame,
    title: str,
    output_path: Path,
    annotation_offset: tuple[int, int],
) -> None:
    distance = profile[DISTANCE_FIELD].to_numpy(dtype=float)
    dsm = profile[DSM_FIELD].to_numpy(dtype=float)
    base = profile[BASE_FIELD].to_numpy(dtype=float)
    height = profile[HEIGHT_FIELD].to_numpy(dtype=float)

    valid_dsm = np.isfinite(distance) & np.isfinite(dsm)
    valid_base = np.isfinite(distance) & np.isfinite(base)
    valid_fill = (
        np.isfinite(distance)
        & np.isfinite(dsm)
        & np.isfinite(base)
        & np.isfinite(height)
    )

    if not np.any(valid_dsm):
        raise ValueError(f"No valid DSM samples available for {title}")

    if not np.any(valid_base):
        raise ValueError(f"No valid TIN-base samples available for {title}")

    fig, ax = plt.subplots(figsize=(12, 6))

    ax.plot(
        distance[valid_dsm],
        dsm[valid_dsm],
        linewidth=2.2,
        label="Observed DSM surface",
    )
    ax.plot(
        distance[valid_base],
        base[valid_base],
        linewidth=2.2,
        label="Estimated TIN base",
    )

    ax.fill_between(
        distance,
        base,
        dsm,
        where=valid_fill,
        interpolate=True,
        alpha=0.28,
        label="Mapped stockpile material",
    )

    if np.any(valid_fill):
        peak_index = np.nanargmax(np.where(valid_fill, height, np.nan))
        peak_distance = distance[peak_index]
        peak_height = height[peak_index]
        peak_elevation = dsm[peak_index]

        ax.annotate(
            f"Max height: {peak_height:.2f} m",
            xy=(peak_distance, peak_elevation),
            xytext=annotation_offset,
            textcoords="offset points",
            fontsize=9,
            ha="left",
            va="top",
            arrowprops={"arrowstyle": "->", "linewidth": 0.8},
        )

    ax.set_title(title)
    ax.set_xlabel("Distance along profile (m)")
    ax.set_ylabel("Elevation (m)")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=200)
    plt.close(fig)

    print(f"Saved: {output_path}")


def main() -> None:
    if not INPUT_CSV.exists():
        raise FileNotFoundError(f"Profile CSV not found: {INPUT_CSV}")

    df = pd.read_csv(INPUT_CSV)

    required_fields = {
        PROFILE_FIELD,
        DISTANCE_FIELD,
        DSM_FIELD,
        BASE_FIELD,
        HEIGHT_FIELD,
    }
    missing_fields = required_fields.difference(df.columns)
    if missing_fields:
        raise ValueError(
            f"Missing required columns: {sorted(missing_fields)}. "
            f"Available columns: {list(df.columns)}"
        )

    longitudinal = prepare_profile(df, "P02_LONG")
    transverse = prepare_profile(df, "P02_CROSS")

    plot_profile(
        longitudinal,
        "Section C-C' — Longitudinal",
        LONGITUDINAL_OUTPUT,
        annotation_offset=(57, 3),
    )
    plot_profile(
        transverse,
        "Section D-D' — Transverse",
        TRANSVERSE_OUTPUT,
        annotation_offset=(57, 3),
    )


if __name__ == "__main__":
    main()