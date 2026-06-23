from pathlib import Path

import numpy as np
import rasterio


# Coefficients from fit_floor_plane.py:
# z = (a * x) + (b * y) + c
A = 0.020881284358
B = -0.004845953072
C = -324.947153669248


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_dsm = (
        project_root
        / "data"
        / "raw"
        / "virtual_surveyor_stockpiles"
        / "Stockpiles"
        / "Zeebrugge Stocks.Ei.tif"
    )

    output_raster = (
        project_root
        / "data"
        / "processed"
        / "p01_estimated_floor_plane.tif"
    )

    if not input_dsm.exists():
        raise FileNotFoundError(f"DSM not found: {input_dsm}")

    output_raster.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(input_dsm) as src:
        profile = src.profile.copy()
        nodata = src.nodata

        profile.update(
            dtype="float32",
            count=1,
            compress="lzw",
            tiled=True,
            nodata=nodata,
        )

        with rasterio.open(output_raster, "w", **profile) as dst:
            for _, window in src.block_windows(1):
                dsm_block = src.read(1, window=window)

                rows, cols = np.indices(
                    (window.height, window.width),
                    dtype=np.float64,
                )

                rows += window.row_off
                cols += window.col_off

                xs, ys = rasterio.transform.xy(
                    src.transform,
                    rows,
                    cols,
                    offset="center",
                )

                x_array = np.asarray(xs, dtype=np.float64).reshape(
                    dsm_block.shape
                )
                y_array = np.asarray(ys, dtype=np.float64).reshape(
                    dsm_block.shape
                )

                floor = (
                    A * x_array
                    + B * y_array
                    + C
                ).astype(np.float32)

                if nodata is not None:
                    invalid = dsm_block == nodata
                    floor[invalid] = nodata

                dst.write(floor, 1, window=window)

    print(f"Created floor raster: {output_raster}")


if __name__ == "__main__":
    main()