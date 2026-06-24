from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
PROFILE_DIR = PROJECT_ROOT / "outputs" / "profiles"


def identify_layer(layer_name: str) -> str:
    if "top_surface" in layer_name:
        return "top"
    if "base_surface" in layer_name:
        return "base"
    if "USGS_LPC" in layer_name:
        return "points"
    return "other"


def plot_profile(
    input_csv: Path,
    output_png: Path,
    title: str,
) -> None:
    df = pd.read_csv(input_csv)
    df["series"] = df["layer"].map(identify_layer)

    top = (
        df[df["series"] == "top"]
        .dropna(subset=["distance", "elevation"])
        .sort_values("distance")
    )
    base = (
        df[df["series"] == "base"]
        .dropna(subset=["distance", "elevation"])
        .sort_values("distance")
    )
    points = (
        df[df["series"] == "points"]
        .dropna(subset=["distance", "elevation"])
        .sort_values("distance")
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(
        top["distance"],
        top["elevation"],
        linewidth=2,
        label="Point-cloud-derived top surface",
    )

    ax.plot(
        base["distance"],
        base["elevation"],
        linewidth=2,
        label="Interpolated base surface",
    )

    ax.scatter(
        points["distance"],
        points["elevation"],
        s=14,
        color="black",
        alpha=0.75,
        label="Original LiDAR samples",
        zorder=3,
    )

    # Interpolate both raster series to a shared distance axis
    # before shading between them.
    merged = pd.merge_asof(
        top[["distance", "elevation"]].rename(
            columns={"elevation": "top_elevation"}
        ),
        base[["distance", "elevation"]].rename(
            columns={"elevation": "base_elevation"}
        ),
        on="distance",
        direction="nearest",
        tolerance=1.0,
    ).dropna()

    ax.fill_between(
        merged["distance"],
        merged["base_elevation"],
        merged["top_elevation"],
        alpha=0.18,
        label="Height above base",
    )

    ax.set_title(title)
    ax.set_xlabel("Distance along profile (ft)")
    ax.set_ylabel("Elevation (ft NAVD88)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    PROFILE_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_png, dpi=300, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    plot_profile(
        TABLE_DIR / "p01_profile_AA.csv",
        PROFILE_DIR / "p01_profile_longitudinal_labeled.png",
        "P01 Longitudinal Profile A–A",
    )

    plot_profile(
        TABLE_DIR / "p01_profile_BB.csv",
        PROFILE_DIR / "p01_profile_transverse_labeled.png",
        "P01 Transverse Profile B–B",
    )


if __name__ == "__main__":
    main()