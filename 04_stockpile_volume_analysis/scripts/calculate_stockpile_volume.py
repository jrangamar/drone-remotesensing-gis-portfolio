from pathlib import Path
import csv

import numpy as np
import rasterio


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]

    input_raster = (
        project_root
        / "data"
        / "processed"
        / "stockpile_height_above_floor.tif"
    )
    cleaned_raster = (
        project_root
        / "data"
        / "processed"
        / "stockpile_height_positive.tif"
    )
    output_csv = (
        project_root
        / "data"
        / "results"
        / "stockpile_metrics.csv"
    )

    if not input_raster.exists():
        raise FileNotFoundError(f"Input raster not found: {input_raster}")

    output_csv.parent.mkdir(parents=True, exist_ok=True)

    with rasterio.open(input_raster) as src:
        height = src.read(1, masked=True).astype(np.float64)
        profile = src.profile.copy()

        pixel_width = abs(src.transform.a)
        pixel_height = abs(src.transform.e)
        pixel_area_m2 = pixel_width * pixel_height

        valid_values = height.compressed()
        if valid_values.size == 0:
            raise ValueError("The input raster contains no valid pixels.")

        negative_pixel_count = int(np.count_nonzero(valid_values < 0))
        minimum_height_before_clamping_m = float(valid_values.min())

        positive_height = np.ma.maximum(height, 0.0)
        positive_values = positive_height.compressed()
        valid_pixel_count = int(positive_values.size)

        footprint_area_m2 = valid_pixel_count * pixel_area_m2
        volume_m3 = float(positive_values.sum() * pixel_area_m2)
        volume_yd3 = volume_m3 * 1.30795062

        mean_height_m = float(positive_values.mean())
        maximum_height_m = float(positive_values.max())

        nodata = src.nodata
        profile.pop("blockxsize", None)
        profile.pop("blockysize", None)
        profile.pop("tiled", None)
        profile.update(
            dtype="float32",
            count=1,
            compress="lzw",
            tiled=False,
            nodata=nodata,
        )

        output_array = positive_height.filled(nodata).astype(np.float32)

        with rasterio.open(cleaned_raster, "w", **profile) as dst:
            dst.write(output_array, 1)

    metrics = {
        "pile_id": "P01",
        "base_method": "least-squares sloping plane from six floor samples",
        "pixel_width_m": pixel_width,
        "pixel_height_m": pixel_height,
        "pixel_area_m2": pixel_area_m2,
        "valid_pixel_count": valid_pixel_count,
        "footprint_area_m2": footprint_area_m2,
        "mean_height_m": mean_height_m,
        "maximum_height_m": maximum_height_m,
        "volume_m3": volume_m3,
        "volume_yd3": volume_yd3,
        "negative_pixel_count_before_clamping": negative_pixel_count,
        "minimum_height_before_clamping_m": minimum_height_before_clamping_m,
    }

    with output_csv.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=metrics.keys())
        writer.writeheader()
        writer.writerow(metrics)

    print("Stockpile volume calculation")
    print(f"Valid pixels: {valid_pixel_count:,}")
    print(f"Pixel area: {pixel_area_m2:.6f} m²")
    print(f"Footprint area: {footprint_area_m2:.2f} m²")
    print(f"Mean positive height: {mean_height_m:.3f} m")
    print(f"Maximum height: {maximum_height_m:.3f} m")
    print(f"Volume: {volume_m3:.2f} m³")
    print(f"Volume: {volume_yd3:.2f} yd³")
    print()
    print(f"Negative pixels clamped to zero: {negative_pixel_count:,}")
    print(
        "Lowest original height: "
        f"{minimum_height_before_clamping_m:.3f} m"
    )
    print()
    print(f"Cleaned raster: {cleaned_raster}")
    print(f"Metrics CSV: {output_csv}")


if __name__ == "__main__":
    main()