

from pathlib import Path

import numpy as np
import pandas as pd
import rasterio
from rasterio.enums import Resampling
from rasterio.warp import reproject


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DSM_PATH = (
    PROJECT_ROOT
    / "data/raw/virtual_surveyor_stockpiles/Stockpiles"
    / "Zeebrugge Stocks.Ei.tif"
)
PLANE_BASE_PATH = PROJECT_ROOT / "data/processed/p02_estimated_plane_base.tif"
HEIGHT_OUTPUT_PATH = (
    PROJECT_ROOT / "data/processed/p02_stockpile_height_above_plane.tif"
)
POSITIVE_OUTPUT_PATH = (
    PROJECT_ROOT / "data/processed/p02_stockpile_height_plane_positive.tif"
)
METRICS_OUTPUT_PATH = PROJECT_ROOT / "data/results/p02_plane_metrics.csv"

OUTPUT_NODATA = -9999.0
CUBIC_METRES_TO_CUBIC_YARDS = 1.30795062


def write_raster(
    path: Path,
    array: np.ndarray,
    profile: dict,
) -> None:
    output_profile = profile.copy()
    output_profile.update(
        driver="GTiff",
        count=1,
        dtype="float32",
        nodata=OUTPUT_NODATA,
        compress="deflate",
        tiled=True,
    )

    with rasterio.open(path, "w", **output_profile) as dst:
        dst.write(array.astype("float32"), 1)


def main() -> None:
    if not DSM_PATH.exists():
        raise FileNotFoundError(f"DSM not found: {DSM_PATH}")

    if not PLANE_BASE_PATH.exists():
        raise FileNotFoundError(f"Plane base not found: {PLANE_BASE_PATH}")

    with rasterio.open(PLANE_BASE_PATH) as plane_src:
        plane = np.asarray(plane_src.read(1), dtype="float64")
        plane_profile = plane_src.profile.copy()
        plane_transform = plane_src.transform
        plane_crs = plane_src.crs
        plane_nodata = plane_src.nodata

        plane_valid = np.isfinite(plane)
        if plane_nodata is not None:
            plane_valid &= plane != plane_nodata

        dsm_aligned = np.full(plane.shape, np.nan, dtype="float64")

        with rasterio.open(DSM_PATH) as dsm_src:
            reproject(
                source=rasterio.band(dsm_src, 1),
                destination=dsm_aligned,
                src_transform=dsm_src.transform,
                src_crs=dsm_src.crs,
                src_nodata=dsm_src.nodata,
                dst_transform=plane_transform,
                dst_crs=plane_crs,
                dst_nodata=np.nan,
                resampling=Resampling.bilinear,
            )

    valid = plane_valid & np.isfinite(dsm_aligned)

    if not np.any(valid):
        raise RuntimeError("No overlapping valid DSM and plane pixels were found.")

    height = np.full(plane.shape, OUTPUT_NODATA, dtype="float64")
    height[valid] = dsm_aligned[valid] - plane[valid]

    valid_heights = height[valid]
    negative_mask = valid & (height < 0)
    negative_count = int(np.count_nonzero(negative_mask))
    minimum_before_clamp = float(np.min(valid_heights))

    positive_height = np.full(plane.shape, OUTPUT_NODATA, dtype="float64")
    positive_height[valid] = np.maximum(height[valid], 0.0)

    positive_values = positive_height[valid]
    positive_only = positive_values[positive_values > 0]

    pixel_width = abs(plane_transform.a)
    pixel_height = abs(plane_transform.e)
    pixel_area = pixel_width * pixel_height

    valid_pixel_count = int(np.count_nonzero(valid))
    positive_pixel_count = int(np.count_nonzero(positive_values > 0))
    footprint_area = valid_pixel_count * pixel_area
    positive_area = positive_pixel_count * pixel_area
    volume_m3 = float(np.sum(positive_values) * pixel_area)
    volume_yd3 = volume_m3 * CUBIC_METRES_TO_CUBIC_YARDS
    mean_positive_height = float(np.mean(positive_only))
    maximum_height = float(np.max(positive_values))

    write_raster(HEIGHT_OUTPUT_PATH, height, plane_profile)
    write_raster(POSITIVE_OUTPUT_PATH, positive_height, plane_profile)

    metrics = pd.DataFrame(
        [
            {
                "pile_id": "P02",
                "base_model": "least_squares_plane",
                "valid_pixel_count": valid_pixel_count,
                "positive_pixel_count": positive_pixel_count,
                "pixel_area_m2": pixel_area,
                "footprint_area_m2": footprint_area,
                "positive_area_m2": positive_area,
                "mean_positive_height_m": mean_positive_height,
                "maximum_height_m": maximum_height,
                "volume_m3": volume_m3,
                "volume_yd3": volume_yd3,
                "negative_pixel_count_before_clamp": negative_count,
                "minimum_height_before_clamp_m": minimum_before_clamp,
            }
        ]
    )
    metrics.to_csv(METRICS_OUTPUT_PATH, index=False)

    print(f"Valid pixels: {valid_pixel_count:,}")
    print(f"Positive pixels: {positive_pixel_count:,}")
    print(f"Pixel area: {pixel_area:.6f} m²")
    print(f"Footprint area: {footprint_area:.3f} m²")
    print(f"Positive area: {positive_area:.3f} m²")
    print(f"Mean positive height: {mean_positive_height:.3f} m")
    print(f"Maximum height: {maximum_height:.3f} m")
    print(f"Volume: {volume_m3:.3f} m³")
    print(f"Volume: {volume_yd3:.3f} yd³")
    print(f"Negative pixels before clamping: {negative_count:,}")
    print(f"Minimum height before clamping: {minimum_before_clamp:.3f} m")
    print(f"Saved: {HEIGHT_OUTPUT_PATH}")
    print(f"Saved: {POSITIVE_OUTPUT_PATH}")
    print(f"Saved: {METRICS_OUTPUT_PATH}")


if __name__ == "__main__":
    main()