

# Data Source

## Dataset

This project uses a public USGS 3DEP airborne LiDAR point-cloud tile covering part of an industrial area in Miami-Dade County, Florida.

- Dataset title: `USGS Lidar Point Cloud FL_MiamiDade_D23 LID2024_316038_0901`
- Publisher and originator: U.S. Geological Survey
- Product type: LiDAR Point Cloud (LPC)
- File format: LAZ, compressed LAS
- ScienceBase item: https://www.sciencebase.gov/catalog/item/68b8e5a0d4be0247d9626f90
- Source filename: `USGS_LPC_FL_MiamiDade_D23_LID2024_316038_0901.laz`

## Dates

The ScienceBase record reports:

- Acquisition start: 2023-12-27
- Acquisition end: 2024-05-29
- Publication date: 2025-09-02
- File modification date: 2025-09-03

The project refers to the source as the **2024 Miami-Dade LiDAR dataset** because the selected tile was collected during the 2024 portion of the acquisition and its source filename identifies it as `LID2024`.

## Download and metadata

The LAZ tile was identified and downloaded through the USGS 3DEP LiDAR Explorer and The National Map distribution system. The ScienceBase record provides the authoritative catalog entry, original product metadata, browse image, and LAZ download resource.

Relevant source resources:

- ScienceBase catalog record: https://www.sciencebase.gov/catalog/item/68b8e5a0d4be0247d9626f90
- Original product metadata: https://thor-f5.er.usgs.gov/ngtoc/metadata/waf/elevation/lidar_point_cloud/laz/FL_MiamiDade_1_D23/USGS_LPC_FL_MiamiDade_D23_LID2024_316038_0901.xml
- Browse image: https://prd-tnm.s3.amazonaws.com/StagedProducts/Elevation/LPC/Projects/FL_MiamiDade_D23/FL_MiamiDade_1_D23/browse/USGS_LPC_FL_MiamiDade_D23_LID2024_316038_0901.jpg
- LAZ download: https://rockyweb.usgs.gov/vdelivery/Datasets/Staged/Elevation/LPC/Projects/FL_MiamiDade_D23/FL_MiamiDade_1_D23/LAZ/USGS_LPC_FL_MiamiDade_D23_LID2024_316038_0901.laz

## Coordinate reference systems

Inspection in QGIS identified the following reference systems:

- Horizontal CRS: NAD83(2011) / Florida East (ftUS), EPSG:6438
- Vertical CRS: NAVD88 height (ftUS), EPSG:6360

The project preserves these native US survey-foot units so that elevations, profile distances, heights, and volume calculations remain internally consistent.

## Source-tile characteristics

The downloaded LAZ tile contains:

- 28,419,282 points;
- horizontal extent from approximately 855,000 to 860,000 ft Easting;
- horizontal extent from approximately 565,000 to 570,000 ft Northing;
- elevation range of approximately -5.22 to 125.58 ft;
- LAS version 1.4;
- discrete-return LiDAR attributes including intensity, return information, classification, scan angle, and GPS time.

The source metadata embedded in the tile identifies `Leica TerrainMapper` as the system and `GeoCue LAS Updater` as the software ID.

## Source classification

The full source tile includes the following classes:

| Class | Description |
|---:|---|
| 1 | Unclassified |
| 2 | Ground |
| 7 | Low Point / Noise |
| 9 | Water |
| 17 | Bridge Deck |
| 18 | High Noise |
| 20 | Reserved |

The full-tile statistics viewed in QGIS were approximately:

| Class | Percentage |
|---:|---:|
| 1 — Unclassified | 61.7% |
| 2 — Ground | 37.6% |
| 7 — Low Point / Noise | 0.1% |
| 9 — Water | 0.1% |
| 17 — Bridge Deck | 0.4% |
| 18 — High Noise | less than 0.1% |
| 20 — Reserved | less than 0.1% |

These QGIS statistics are estimated from sampled data and were used for initial inspection rather than as final authoritative counts.

## Project subset

A single stockpile, P01, was selected from the source tile. The clipped P01 point cloud contained 10,493 points:

| Classification | Count | Percentage |
|---|---:|---:|
| Unclassified | 3,105 | 29.59% |
| Ground | 7,388 | 70.41% |

Visual inspection showed that much of the stockpile surface had been classified as ground. This classification issue is central to the project methodology: the supplied Class 2 points were reviewed, but an independently modeled local base surface was used for the volume calculation.

## Why this dataset was suitable

The source was selected because it provides:

- public LAS/LAZ point-cloud data from a real industrial setting;
- sufficient local density for pile-scale terrain modeling;
- documented classification and return attributes;
- native vertical elevations suitable for profile and volume analysis;
- a clear opportunity to demonstrate classification review rather than assuming the supplied labels were correct.

The point density is lower than a typical close-range drone photogrammetry or site-survey point cloud, but it is adequate for demonstrating a defensible public-data workflow at the scale of the selected stockpile.

## Citation

Recommended source citation:

> U.S. Geological Survey. 2025. *USGS Lidar Point Cloud FL_MiamiDade_D23 LID2024_316038_0901*. U.S. Geological Survey, The National Map, 3D Elevation Program.

## License and repository handling

The source data are public USGS elevation data. The original LAZ tile is not committed to the Git repository because of its file size. The repository instead preserves:

- the authoritative catalog and download links;
- source metadata and coordinate-reference information;
- small derived summary tables;
- final figures;
- scripts and documentation needed to understand and reproduce the workflow.