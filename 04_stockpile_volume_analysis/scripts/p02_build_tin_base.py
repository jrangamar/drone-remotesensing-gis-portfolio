from pathlib import Path

import geopandas as gpd
import numpy as np
import rasterio
from rasterio.features import geometry_mask
from rasterio.transform import xy
from rasterio.windows import from_bounds
from scipy.interpolate import LinearNDInterpolator


PROJECT_ROOT = Path(__file__).resolve().parents[1]

GPKG_PATH = PROJECT_ROOT / "data/processed/stockpile_analysis.gpkg"
DSM_PATH = (
    PROJECT_ROOT
    / "data/raw/virtual_surveyor_stockpiles/Stockpiles"
    / "Zeebrugge Stocks.Ei.tif"
)
OUTPUT_PATH = PROJECT_ROOT / "data/processed/p02_estimated_tin_base.tif"

CONTROL_LAYER = "p02_tin_control_points"
BOUNDARY_LAYER = "p02_stockpile_boundary"

ELEVATION_FIELD = "dsm_1"
OUTPUT_NODATA = -9999.0


def main() -> None:
    controls = gpd.read_file(GPKG_PATH, layer=CONTROL_LAYER)
    boundary = gpd.read_file(GPKG_PATH, layer=BOUNDARY_LAYER)

    if controls.empty:
        raise ValueError(f"No features found in {CONTROL_LAYER}")

    if len(boundary) != 1:
        raise ValueError(
            f"{BOUNDARY_LAYER} must contain exactly one polygon; "
            f"found {len(boundary)}"
        )

    if ELEVATION_FIELD not in controls.columns:
        raise ValueError(
            f"Missing elevation field '{ELEVATION_FIELD}' "
            f"in {CONTROL_LAYER}"
        )

    if controls.crs != boundary.crs:
        boundary = boundary.to_crs(controls.crs)

    controls = controls.dropna(subset=[ELEVATION_FIELD]).copy()

    x_control = controls.geometry.x.to_numpy()
    y_control = controls.geometry.y.to_numpy()
    z_control = controls[ELEVATION_FIELD].to_numpy(dtype=float)

    interpolation_points = np.column_stack([x_control, y_control])
    interpolator = LinearNDInterpolator(
        interpolation_points,
        z_control,
        fill_value=np.nan,
    )

    boundary_geometry = boundary.geometry.iloc[0]

    with rasterio.open(DSM_PATH) as dsm:
        if dsm.crs != controls.crs:
            raise ValueError(
                "DSM CRS does not match the control-point CRS: "
                f"{dsm.crs} versus {controls.crs}"
            )

        min_x, min_y, max_x, max_y = boundary_geometry.bounds

        window = from_bounds(
            min_x,
            min_y,
            max_x,
            max_y,
            transform=dsm.transform,
        )
        window = window.round_offsets().round_lengths()

        window_transform = dsm.window_transform(window)
        height = int(window.height)
        width = int(window.width)

        rows, cols = np.indices((height, width))

        x_grid, y_grid = xy(
            window_transform,
            rows,
            cols,
            offset="center",
        )

        x_grid = np.asarray(x_grid).reshape(height, width)
        y_grid = np.asarray(y_grid).reshape(height, width)

        tin_base = np.asarray(interpolator(x_grid, y_grid)).reshape(
            height,
            width,
        )

        inside_polygon = geometry_mask(
            [boundary_geometry.__geo_interface__],
            out_shape=(height, width),
            transform=window_transform,
            invert=True,
        )

        tin_base[~inside_polygon] = np.nan

        valid_values = tin_base[np.isfinite(tin_base)]

        if valid_values.size == 0:
            raise RuntimeError(
                "TIN interpolation produced no valid pixels inside the boundary."
            )

        output_array = np.where(
            np.isfinite(tin_base),
            tin_base,
            OUTPUT_NODATA,
        ).astype("float32")

        profile = dsm.profile.copy()
        profile.update(
            driver="GTiff",
            height=height,
            width=width,
            count=1,
            dtype="float32",
            transform=window_transform,
            nodata=OUTPUT_NODATA,
            compress="deflate",
            tiled=True,
        )

        with rasterio.open(OUTPUT_PATH, "w", **profile) as output:
            output.write(output_array, 1)

    print(f"Control points used: {len(controls)}")
    print(f"TIN minimum: {valid_values.min():.3f} m")
    print(f"TIN maximum: {valid_values.max():.3f} m")
    print(f"Raster dimensions: {width} × {height} pixels")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()