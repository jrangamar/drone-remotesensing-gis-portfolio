# Drone/Remote Sensing/GIS Portfolio

A portfolio of GIS, photogrammetry, and geospatial web-publishing projects focused on drone imagery, spatial analysis, and reproducible technical workflows.

The projects progress from desktop GIS and cartographic analysis, through photogrammetry processing and interactive web publishing, to raster-based stockpile volume analysis with QGIS and Python.

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

A Python-generated Folium and Leaflet viewer that publishes selected outputs from the earlier projects as a static website.

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

A QGIS and Python workflow for estimating the volume of a contained aggregate stockpile from a public orthomosaic and digital surface model.

The project demonstrates:

- Manual stockpile-footprint interpretation
- Exposed-floor sampling and zonal statistics
- Least-squares reconstruction of a sloping bay floor
- Raster subtraction and positive-height integration
- Stockpile volume estimation in cubic metres and cubic yards
- Sensitivity testing for alternative floor and boundary assumptions
- Longitudinal and transverse profile extraction
- Matplotlib cross-section plotting
- Final cartographic layout and technical documentation

Primary estimate:

- Footprint area: 75.70 m²
- Maximum height: 2.89 m
- Estimated volume: 120.55 m³ / 157.67 yd³

Project directory:

```text
04_stockpile_volume_analysis/
```

## Portfolio Progression

```text
QGIS mapping and cartography
      ↓
Drone photogrammetry processing
      ↓
Python and web geospatial publishing
      ↓
Raster-based volume analysis and uncertainty checks
```

Together, these projects demonstrate a workflow that moves from spatial data preparation and cartography to imagery processing, public-facing presentation, quantitative surface analysis, and reproducible technical reporting.

## Repository Structure

```text
GIS_portfolio/
├── 01_south_florida_qgis_map/
├── 02_photogrammetry/
├── 03_interactive_geospatial_viewer/
├── 04_stockpile_volume_analysis/
├── .github/
│   └── workflows/
├── .gitignore
└── README.md
```

Each project directory contains its own documentation, data organization, scripts, outputs, or supporting notes as appropriate.

## Tools and Technologies

- QGIS
- GDAL
- Rasterio
- NumPy
- pandas
- Matplotlib
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
- Cross-section analysis
- Sensitivity testing for modeling assumptions

Possible future work may explore point-cloud inspection, LiDAR processing, additional remote-sensing methods, and 3D geospatial visualization.

## Author

Journey Rangamar
