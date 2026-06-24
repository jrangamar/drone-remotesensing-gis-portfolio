# Workflow

## 1. Source data acquisition

A 2024 USGS 3DEP LAZ tile covering an industrial site in Miami-Dade County was downloaded from the 3DEP LiDAR Explorer. The source point cloud was retained in its native horizontal and vertical reference systems:

- Horizontal CRS: NAD83(2011) / Florida East (ftUS), EPSG:6438
- Vertical datum: NAVD88 height (ftUS), EPSG:6360

The source tile contains more than 28 million points. Initial review included point count, coordinate extent, classification distribution, return information, elevation range, and visual inspection in both 2D and 3D.

## 2. Target stockpile selection

A single free-standing stockpile, identified as P01, was selected because it had:

- a clearly defined toe;
- relatively open surrounding ground;
- sufficient point coverage;
- limited interference from structures or retaining walls;
- a shape suitable for longitudinal and transverse profiling.

The pile boundary was digitized manually in QGIS and refined using the 3D point-cloud view.

## 3. Classification review

The clipped P01 point cloud contained 10,493 points:

- 3,105 unclassified points, or 29.59%;
- 7,388 ground-classified points, or 70.41%.

Visual review showed that much of the stockpile surface itself had been assigned to the ground class. For that reason, the supplied Class 2 points were not used directly as the local base surface.

## 4. Floor-control sampling

Eight floor-control polygons were digitized around the pile on surrounding yard surfaces. Point elevations were sampled within each polygon and summarized using the median to reduce sensitivity to outliers.

The resulting control elevations ranged from approximately 7.40 ft to 9.90 ft NAVD88 and showed a gradual west-to-east slope across the yard.

The control polygons were converted to centroids, joined with their median elevation values, and saved as spatial floor-control points.

## 5. Base-surface construction

A linear TIN interpolation was created from the eight floor-control points using the median elevation field. The interpolated surface was clipped to the P01 boundary and used as the preferred sloping base surface.

A second constant-floor model was also created using the median of the eight floor-control elevations:

- Constant floor elevation: 8.005 ft NAVD88

This alternate surface was used for sensitivity testing.

## 6. Point-cloud top surface

The clipped P01 point cloud was exported to a 1 ft raster using the Z attribute. The resulting top-surface raster was aligned to the base-surface grid so that both rasters shared the same coordinate system, cell alignment, and analysis footprint.

NoData values were preserved and handled explicitly to prevent invalid cells from being included in the height and volume calculations.

## 7. Height-above-base calculation

Height above base was calculated as:

```text
height = top surface - base surface
```

Negative values were set to zero. Two matched-footprint rasters were created:

- sloping-TIN height above base;
- constant-floor height above base.

Both final comparison rasters contained 11,838 valid cells.

## 8. Volume calculation

Raster volume was calculated from the sum of height values multiplied by raster cell area:

```text
volume_ft3 = raster_sum × cell_area_ft2
volume_yd3 = volume_ft3 / 27
```

Using a cell area of approximately 0.997948606 ft², the preferred sloping-base result was:

- 114,403.88 ft³
- 4,237.18 yd³

The constant-floor result was:

- 117,753.61 ft³
- 4,361.24 yd³

The constant-floor estimate was 2.93% higher than the preferred TIN-based result, indicating relatively low sensitivity to the tested base assumption.

## 9. Point-density review

A 1 ft point-density raster was generated and clipped to the stockpile boundary. The clipped density statistics were:

- 11,833 valid cells;
- 10,449 total points represented;
- mean density: 0.883 points/ft²;
- mean density: approximately 9.50 points/m²;
- maximum density: 2 points/ft².

The small difference between the density-raster cell count and the height-raster cell count resulted from their slightly different raster grids and boundary-cell inclusion.

## 10. Profile extraction

Two profile lines were digitized across the pile:

- A–A: longitudinal profile;
- B–B: transverse profile.

QGIS Elevation Profile was used to sample the aligned top surface, interpolated base surface, and original LiDAR observations. The profile data were exported to CSV and replotted with Python using pandas and matplotlib.

The final figures show:

- point-cloud-derived top surface;
- interpolated base surface;
- original LiDAR samples;
- shaded height above base.

## 11. Production deliverables

Final deliverables include:

- one-page height and volume production map;
- longitudinal A–A profile;
- transverse B–B profile;
- 3D point-cloud review image;
- classification summary CSV;
- density summary CSV;
- volume comparison CSV;
- reproducible Python plotting script.

## 12. Software

- QGIS 3.44.10
- GDAL 3.12.3
- PDAL 2.9.3
- Python 3.14
- pandas
- matplotlib

## 13. Limitations

The final volume is an analytical estimate rather than a survey-certified quantity. It depends on:

- interpretation of the stockpile toe;
- point-cloud density and classification quality;
- rasterization and alignment choices;
- the eight selected floor-control samples;
- the assumption that the interpolated surface reasonably represents the ground beneath the pile.

The sensitivity result helps quantify one part of that uncertainty but does not remove all possible error sources.
