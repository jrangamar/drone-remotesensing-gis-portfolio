# Drone/Remote Sensing/GIS Portfolio

A portfolio of GIS, photogrammetry, LiDAR, and geospatial web-publishing projects focused on drone imagery, point clouds, spatial analysis, and reproducible technical workflows.

The projects progress from desktop GIS and cartographic analysis, through photogrammetry processing and interactive web publishing, to raster- and point-cloud-based stockpile volume analysis with QGIS and Python.

## Live Interactive Viewer

[Open the interactive geospatial viewer](https://jrangamar.github.io/drone-remotesensing-gis-portfolio/)

## Project Overview

### 01 — South Florida QGIS Map

A site-context mapping project centered on Arch Creek Park in Miami-Dade County.

The project demonstrates:

- QGIS project setup and layer management
- Coordinate reference system selection and reprojection
- Vector data preparation
- Site buffers and local context analysis
- Labeling and cartographic styling
- Final static map layout

Project directory:

```text
01_south_florida_qgis_map/
```

### 02 — Photogrammetry Case Studies

A WebODM-based photogrammetry project using two public drone-image datasets:

- Sand Key
- Helenenschacht

The project demonstrates:

- Docker-based WebODM operation
- Drone-image reconstruction
- Orthophoto and DSM generation
- Hillshade and contour creation in QGIS
- Slope and terrain-product review
- Point-cloud and 3D-output inspection
- Resource troubleshooting
- Recovery from an out-of-memory meshing failure
- Comparison of coastal and structural datasets

Project directory:

```text
02_photogrammetry/
```

### 03 — Interactive Geospatial Viewer

A Python-generated Folium and Leaflet viewer that publishes selected outputs from completed projects as a static website.

The project demonstrates:

- Python geospatial preprocessing
- GeoJSON project locations and area polygons
- Folium and Leaflet map generation
- Custom JavaScript interaction
- Popup image carousels and expanded previews
- Coordinated marker and polygon highlighting
- Responsive popup positioning
- Static-site packaging
- GitHub Pages deployment through GitHub Actions

Project directory:

```text
03_interactive_geospatial_viewer/
```

Live site:

[https://jrangamar.github.io/drone-remotesensing-gis-portfolio/](https://jrangamar.github.io/drone-remotesensing-gis-portfolio/)

### 04 — Stockpile Volume and Cross-Section Analysis

A QGIS and Python workflow for estimating stockpile volume from a public orthomosaic and digital surface model, using two contrasting aggregate piles.

The project demonstrates:

- Manual stockpile-footprint interpretation
- Exposed-floor and perimeter-elevation sampling
- Least-squares reconstruction of a sloping bay floor
- Perimeter-based TIN reconstruction for a large freestanding pile
- Review and exclusion of non-ground elevation artifacts
- Raster subtraction and positive-height integration
- Stockpile volume estimation in cubic metres and cubic yards
- Sensitivity testing for alternative base surfaces and boundaries
- Longitudinal and transverse profile extraction
- Matplotlib cross-section plotting
- Final cartographic layouts and technical documentation

Primary results:

- **P01 — contained stockpile:** 75.70 m² footprint, 2.89 m maximum height, and 120.55 m³ / 157.67 yd³ estimated volume using a fitted sloping floor plane.
- **P02 — freestanding stockpile:** 1,207.32 m² footprint, 10.74 m maximum height, and 4,412.86 m³ / 5,771.80 yd³ estimated volume using a cleaned perimeter TIN.

The P02 fitted-plane sensitivity case produced 4,493.58 m³, a difference of +1.83% from the primary TIN estimate.

Project directory:

```text
04_stockpile_volume_analysis/
```

### 05 — Point-Cloud Stockpile Height and Volume Analysis

A QGIS and Python workflow for estimating stockpile volume directly from a public USGS 3DEP LiDAR point cloud at an industrial site in Miami-Dade County.

The project demonstrates:

- LAS/LAZ metadata, classification, return, and 3D inspection
- Target-stockpile selection and manual toe delineation
- Review of unreliable supplied ground classification
- Local floor-control sampling around the stockpile
- Sloping TIN base-surface reconstruction
- Point-cloud rasterization and grid alignment
- Explicit NoData and raster-footprint handling
- Height-above-base and volume calculation
- Constant-floor sensitivity testing
- Point-density and classification QA
- Longitudinal and transverse profile validation
- Python plotting of modeled surfaces and original LiDAR samples
- Final production mapping and reproducible documentation

Primary result:

- **P01 — free-standing stockpile:** 30.85 ft maximum height and **4,237.18 yd³** estimated volume using a sloping TIN base derived from eight surrounding floor-control samples.

A constant-floor comparison produced **4,361.24 yd³**, a difference of **+2.93%** from the preferred estimate. The clipped point cloud had a mean density of approximately **0.88 points/ft²** or **9.5 points/m²**.

Project directory:

```text
05_point_cloud_stockpile_analysis/
```

## Portfolio Progression

```text
QGIS mapping and cartography
      ↓
Drone photogrammetry processing
      ↓
Python and web geospatial publishing
      ↓
Raster-based volume analysis and surface reconstruction
      ↓
Direct LiDAR point-cloud inspection, QA, and volume modeling
```

Together, these projects demonstrate a workflow that moves from spatial data preparation and cartography to imagery processing, public-facing presentation, quantitative surface reconstruction, direct point-cloud analysis, uncertainty testing, and reproducible technical reporting.

## Repository Structure

```text
GIS_portfolio/
├── 01_south_florida_qgis_map/
├── 02_photogrammetry/
├── 03_interactive_geospatial_viewer/
├── 04_stockpile_volume_analysis/
├── 05_point_cloud_stockpile_analysis/
├── .github/
│   └── workflows/
├── .gitignore
└── README.md
```

Each project directory contains its own documentation, data organization, scripts, outputs, or supporting notes as appropriate.

## Tools and Technologies

- QGIS
- GDAL
- PDAL
- LAS/LAZ and COPC
- Rasterio
- NumPy
- pandas
- Matplotlib
- SciPy
- Shapely
- PyProj
- Python
- GeoPandas
- Folium
- Leaflet
- GeoJSON
- WebODM
- Docker
- Git
- GitHub
- GitHub Actions
- GitHub Pages

## Data and Storage Notes

Large raw drone-image datasets and full processing outputs are excluded where they are impractical for a public Git repository.

The repository emphasizes:

- Reproducible scripts
- Lightweight derived products
- Web-ready preview assets
- Project documentation
- Selected screenshots and outputs

Source datasets and external GIS layers are credited within the relevant project documentation.

## Current Scope

This repository currently focuses on:

- GIS mapping and cartography
- Drone photogrammetry
- Raster and vector analysis
- Terrain and surface-product review
- Interactive geospatial publishing
- Stockpile volume estimation
- LiDAR point-cloud inspection and classification review
- Point-cloud rasterization and density assessment
- Plane- and TIN-based surface reconstruction
- Local base-surface modeling from floor-control samples
- Cross-section analysis
- Sensitivity testing for modeling assumptions

Possible future work may extend the point-cloud workflow to additional LiDAR terrain and structure analyses, multi-date surface comparison, other remote-sensing methods, and deeper 3D geospatial visualization.

## Author

Journey Rangamar
