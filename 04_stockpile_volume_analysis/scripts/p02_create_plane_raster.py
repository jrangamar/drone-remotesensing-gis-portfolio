

from pathlib import Path
import re

import numpy as np
import rasterio
from rasterio.transform import xy


PROJECT_ROOT = Path(__file__).resolve().parents[1]

EQUATION_PATH = PROJECT_ROOT / "data/results/p02_plane_equation.txt"
TEMPLATE_RASTER_PATH = PROJECT_ROOT / "data/processed/p02_estimated_tin_base.tif"
OUTPUT_PATH = PROJECT_ROOT / "data/processed/p02_estimated_plane_base.tif"

OUTPUT_NODATA = -9999.0


def read_plane_coefficients(path: Path) -> tuple[float, float, float]:
    if not path.exists():
        raise FileNotFoundError(f"Plane equation file not found: {path}")

    text = path.read_text(encoding="utf-8")

    pattern = re.compile(
        r"z\s*=\s*\(([-+0-9.eE]+)\s*\*\s*x\)\s*"
        r"\+\s*\(([-+0-9.eE]+)\s*\*\s*y\)\s*"
        r"\+\s*\(([-+0-9.eE]+)\)"
    )
    match = pattern.search(text)

    if match is None:
        raise ValueError(
            "Could not parse plane coefficients from "
            f"{path}. Expected a line like: "
            "z = (a * x) + (b * y) + (c)"
        )

    return tuple(float(value) for value in match.groups())


def main() -> None:
    if not TEMPLATE_RASTER_PATH.exists():
        raise FileNotFoundError(
            f"Template raster not found: {TEMPLATE_RASTER_PATH}"
        )

    a, b, c = read_plane_coefficients(EQUATION_PATH)

    with rasterio.open(TEMPLATE_RASTER_PATH) as template:
        template_data = template.read(1)
        profile = template.profile.copy()
        transform = template.transform
        nodata = template.nodata
        height = template.height
        width = template.width

        valid_mask = np.isfinite(template_data)
        if nodata is not None:
            valid_mask &= template_data != nodata

        rows, cols = np.indices((height, width))
        x_grid, y_grid = xy(
            transform,
            rows,
            cols,
            offset="center",
        )

        x_grid = np.asarray(x_grid).reshape(height, width)
        y_grid = np.asarray(y_grid).reshape(height, width)

        plane = (a * x_grid) + (b * y_grid) + c

        output = np.full((height, width), OUTPUT_NODATA, dtype="float32")
        output[valid_mask] = plane[valid_mask].astype("float32")

        valid_values = output[valid_mask]
        if valid_values.size == 0:
            raise RuntimeError("No valid pixels were found in the template mask.")

        profile.update(
            driver="GTiff",
            count=1,
            dtype="float32",
            nodata=OUTPUT_NODATA,
            compress="deflate",
            tiled=True,
        )

        with rasterio.open(OUTPUT_PATH, "w", **profile) as dst:
            dst.write(output, 1)

    print(
        "Plane equation: "
        f"z = ({a:.12f} * x) + ({b:.12f} * y) + ({c:.12f})"
    )
    print(f"Raster dimensions: {width} × {height} pixels")
    print(f"Plane minimum: {valid_values.min():.3f} m")
    print(f"Plane maximum: {valid_values.max():.3f} m")
    print(f"Saved: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()