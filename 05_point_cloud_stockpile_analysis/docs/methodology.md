

# Methodology

## Overview

This project estimates the volume of a free-standing stockpile from public airborne LiDAR. The core methodological problem is that the source classification could not be accepted without review: approximately 70% of the points inside the selected pile boundary were labeled as ground, including much of the stockpile itself. A local base surface therefore had to be modeled independently from surrounding floor elevations.

The preferred estimate uses a point-cloud-derived top surface and a sloping TIN base surface. A constant-floor model provides a sensitivity comparison.

## Source point cloud

The analysis uses a 2024 USGS 3DEP LAZ tile collected over an industrial site in Miami-Dade County, Florida.

Reference systems:

- Horizontal CRS: NAD83(2011) / Florida East (ftUS), EPSG:6438
- Vertical datum: NAVD88 height (ftUS), EPSG:6360

The source tile contains more than 28 million points. Initial inspection covered:

- point count and extent;
- elevation range;
- intensity;
- return number and number of returns;
- classification distribution;
- scan-angle information;
- 2D and 3D visual review.

## Target selection

The selected stockpile, P01, was chosen because it is relatively isolated, has a clearly visible toe, and is surrounded by enough open yard surface to support local floor sampling.

The stockpile boundary was digitized manually in QGIS and checked in the 3D point-cloud viewer. The boundary was intended to follow the visible toe rather than the full rectangular raster extent.

## Classification assessment

Within the clipped P01 point cloud:

| Classification | Count | Percentage |
|---|---:|---:|
| Unclassified | 3,105 | 29.59% |
| Ground | 7,388 | 70.41% |

The classification was unsuitable for direct ground-surface extraction because the stockpile body itself was substantially included in Class 2. Using the supplied ground class as the base would therefore suppress much of the pile height and underestimate volume.

The classification was retained as a QA finding rather than treated as an authoritative terrain model.

## Floor-control samples

Eight floor-control polygons were digitized around the pile on surrounding yard surfaces. Their placement was intended to capture the local grade while avoiding the stockpile toe and obvious non-floor features.

Point elevations within each sample polygon were summarized using the median. Median values were preferred over means because they are less sensitive to isolated high or low returns.

The sampled floor elevations were:

| Sample | Position | Median elevation (ft NAVD88) |
|---|---|---:|
| F01 | North | 8.12 |
| F02 | Northeast | 7.68 |
| F03 | East | 7.75 |
| F04 | Southeast | 7.40 |
| F05 | South | 7.89 |
| F06 | Southwest | 9.54 |
| F07 | West | 9.57 |
| F08 | Northwest | 9.90 |

These values indicate a gradual west-to-east slope across the yard.

## Preferred base surface

The eight control samples were converted to centroid points and joined to their median elevation values. A linear TIN interpolation was then generated from those points.

The TIN was clipped to the P01 boundary and used as the preferred base because it preserves the observed local grade instead of forcing the pile onto a level plane.

The preferred base is therefore an inferred surface beneath the pile, constrained by surrounding floor observations rather than by the source Class 2 classification.

## Constant-floor sensitivity model

A second base model used a constant floor elevation of 8.005 ft NAVD88, derived from the median of the eight floor-control elevations.

This model is not preferred, but it provides a straightforward test of how strongly the final volume depends on the local-base assumption.

## Top-surface generation

The clipped P01 point cloud was rasterized from the Z attribute at approximately 1 ft resolution.

The resulting top surface was aligned to the preferred base raster so that both surfaces shared:

- the same CRS;
- the same cell alignment;
- the same analysis extent;
- the same valid-data footprint.

Explicit NoData handling was required because QGIS and GDAL represented invalid cells using large negative sentinel values in intermediate rasters. Those values were excluded before subtraction and statistics were calculated.

## Height-above-base rasters

For the preferred model:

```text
height_sloping = max(top_surface - sloping_TIN_base, 0)
```

For the sensitivity model:

```text
height_constant = max(top_surface - 8.005 ft, 0)
```

Both rasters were masked to the same valid overlap footprint. Each final comparison raster contained 11,838 valid cells.

Negative values were set to zero because they represent cells where interpolation, rasterization, or boundary placement produced a top elevation at or below the estimated base.

## Volume calculation

Volume was computed from raster height values using:

```text
volume_ft3 = sum(height values) × cell area
volume_yd3 = volume_ft3 / 27
```

The aligned raster cell area was approximately:

```text
0.997948606 ft²
```

### Preferred sloping-base result

- Raster sum: 114,639.0467
- Volume: 114,403.88 ft³
- Volume: 4,237.18 yd³

### Constant-floor result

- Raster sum: 117,995.6608
- Volume: 117,753.61 ft³
- Volume: 4,361.24 yd³

### Sensitivity difference

- Difference: 124.06 yd³
- Difference: +2.93%

The relatively small difference suggests that the volume estimate is not highly sensitive to the tested constant-floor alternative, although the sloping TIN remains the more defensible base model.

## Point-density assessment

A 1 ft point-density raster was created and clipped to the P01 boundary.

Summary statistics:

- Valid cells: 11,833
- Total points represented: 10,449
- Mean density: 0.883 points/ft²
- Mean density: approximately 9.50 points/m²
- Maximum density: 2 points/ft²

The density raster has five fewer valid cells than the height rasters because it was generated on a slightly different grid. The difference occurs along the polygon boundary and does not affect the volume calculation.

## Profile validation

Two profiles were used:

- A–A, longitudinal;
- B–B, transverse.

The QGIS Elevation Profile tool sampled:

- the aligned top-surface raster;
- the clipped TIN base raster;
- original LiDAR observations along each line.

The exported CSVs were replotted in Python. The final figures compare the modeled top and base surfaces with original LiDAR samples and shade the estimated stockpile cross-section.

The close agreement between the original LiDAR samples and the rasterized top surface supports the use of the top raster for volume estimation.

## Interpretation

The preferred result is:

> **4,237 yd³ using a sloping TIN base surface.**

The constant-floor estimate is 2.93% higher. This difference is small enough to support the general stability of the result while still demonstrating that base-surface choice is a measurable source of uncertainty.

## Uncertainty and limitations

The result should be interpreted as an analytical estimate, not a survey-certified quantity. Important uncertainty sources include:

- manual interpretation of the pile toe;
- incomplete or imperfect source classification;
- point density and acquisition geometry;
- raster cell size and alignment;
- interpolation from only eight floor-control samples;
- the assumption that the surrounding floor trend continues beneath the pile;
- edge effects and NoData handling.

The constant-floor sensitivity comparison addresses only one of these uncertainties. It does not represent a complete error budget.

## Reproducibility

The project preserves:

- the QGIS project;
- analysis geometry;
- summary CSVs;
- exported profile CSVs;
- the Python plotting script;
- final figures;
- software dependencies in `requirements.txt`.

Large raw and intermediate point-cloud and raster files are excluded from version control where appropriate.