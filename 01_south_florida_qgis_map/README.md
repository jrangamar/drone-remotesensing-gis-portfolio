# Arch Creek Park 250 m Site Context Map

## Project Overview

This beginner GIS project uses QGIS to create a site context map for Arch Creek Park in North Miami Beach, Florida. The map shows the park boundary, a 250-meter context buffer, and nearby streets within that buffer using public GIS data and an OpenStreetMap basemap.

The purpose of the project is to practice foundational GIS skills that are relevant to drone imagery planning, geospatial site review, and constraint-awareness workflows. This project is not a flight authorization map, and no drone operation is implied.

## Final Map

**Title:** Arch Creek Park 250 m Site Context Map

The final map includes:

- Arch Creek Park boundary
- 250 m context buffer
- Streets within 250 m of the park boundary
- OpenStreetMap basemap
- Scale bar
- North arrow
- Legend
- Data source and CRS note
- Drone authorization disclaimer

## Project Purpose

The goal of this project was to learn how GIS can be used to evaluate the surroundings of a site before any field operation, imagery collection, or drone-related planning decision. A public park was chosen because it provides a compact study area with real-world geospatial complexity, including roads, waterways, vegetation, surrounding development, and public-use constraints.

The 250 m buffer was used to focus on the immediate site context around the park. This distance was chosen because it captures nearby roads, water features, access corridors, and surrounding urban development without expanding the analysis into a broader neighborhood-scale study.

This project is framed as a GIS site-context and constraint-awareness exercise, not as an actual drone flight plan.

## Skills Demonstrated

This project demonstrates the following beginner GIS skills:

- Loading public vector datasets into QGIS
- Working with polygon and line layers
- Inspecting coordinate reference systems
- Selecting a single feature from a larger dataset
- Exporting selected features as a new layer
- Reprojecting data from EPSG:4326 to EPSG:26917
- Creating a distance-based buffer in meters
- Clipping street features to a buffer polygon
- Styling vector layers with basic symbology
- Creating a print layout
- Adding a legend, scale bar, north arrow, title, subtitle, and data note
- Exporting final map products as PNG and PDF

## Data Sources

### Miami-Dade County Park Boundaries

- Geometry type: Polygon
- Original CRS: EPSG:4326 - WGS 84
- Useful fields used/observed:
  - NAME
  - ADDRESS
  - TOTACRE

This layer was used to identify and select Arch Creek Park from the larger Miami-Dade County parks dataset.

### Miami-Dade County Streets

- Geometry type: Line
- Original CRS: EPSG:4326 - WGS 84
- Useful fields used/observed:
  - ST_NAME
  - ST_TYPE
  - LMUNIC_NAME

This layer was used to show nearby street context and was later clipped to the 250 m buffer.

### OpenStreetMap Basemap

OpenStreetMap was used as a visual basemap to provide general geographic context, including roads, buildings, water features, and surrounding neighborhoods.

## Coordinate Reference Systems

The original park and street datasets were loaded in:

- EPSG:4326 - WGS 84

Because EPSG:4326 uses latitude and longitude degrees, it is not ideal for distance-based analysis such as meter-based buffers. For the buffer and clip workflow, the project layers were reprojected into:

- EPSG:26917 - NAD83 / UTM zone 17N

This projected CRS uses meters, allowing the 250 m buffer to represent an actual distance-based analysis zone.

## Workflow

### 1. Load Data

The Miami-Dade County parks layer and streets layer were added to QGIS as vector layers. An OpenStreetMap XYZ tile basemap was also added for visual context.

### 2. Inspect Layer Properties

The layer properties were checked to confirm the geometry type, CRS, and useful attribute fields. The park layer was confirmed as polygon data, and the streets layer was confirmed as line data.

### 3. Select Arch Creek Park

The parks attribute table was searched for the `NAME` value:

`ARCH CREEK PARK`

The selected feature was exported as a standalone layer representing only the Arch Creek Park boundary.

### 4. Reproject Layers

The Arch Creek Park boundary layer and Miami-Dade streets layer were reprojected from EPSG:4326 to EPSG:26917. This was done so distance-based analysis could be performed in meters.

Processed layers included:

- `arch_creek_park_boundary_utm17n`
- `miami_dade_streets_utm17n`

### 5. Create 250 m Buffer

A 250 m buffer was created around the projected Arch Creek Park boundary using QGIS’s Buffer tool.

Output layer:

- `arch_creek_250m_buffer`

The buffer represents an immediate site-context zone around the park. It does not represent a permitted drone flight area.

### 6. Clip Streets to Buffer

The projected Miami-Dade streets layer was clipped using the 250 m buffer as the overlay polygon. This produced a new layer containing only the street segments within the buffer area.

Output layer:

- `streets_within_arch_creek_250m`

This step demonstrates a basic proximity-based spatial analysis workflow.

### 7. Style Layers

The park boundary, buffer, and clipped street layers were styled for readability. The park boundary was emphasized, the 250 m buffer was made transparent enough to preserve basemap visibility, and the clipped streets were styled to show nearby transportation context.

### 8. Create Final Map Layout

A QGIS print layout was created with:

- Map title
- Subtitle
- Legend
- Scale bar
- North arrow
- Data source note
- Projected CRS note
- Drone authorization disclaimer

The map was exported as PNG and PDF.

## Drone / GIS Relevance

This project is relevant to drone imagery and GIS work because it demonstrates how geospatial tools can be used before a field operation or imagery collection task. A site-context map can help identify nearby roads, water features, public-use areas, development patterns, and other features that may affect access, safety, or planning.

The project does not claim that drone flight is permitted from or over Arch Creek Park. Instead, it demonstrates a cautious pre-planning workflow that could support future authorized operations, environmental documentation, public-agency planning, or existing-imagery analysis.

## Limitations

This project is a beginner GIS exercise and has several limitations:

- It does not determine whether drone flight is legally permitted.
- It does not include airspace authorization data.
- It does not include property-owner permission data.
- It does not include live field conditions.
- It does not identify people, temporary hazards, events, or park usage.
- It does not include obstacle-height data.
- It does not include controlled airspace, LAANC, NOTAMs, TFRs, or local drone restrictions.
- It does not replace official flight planning, permitting, or safety review.

## Employer-Facing Summary

This project demonstrates a beginner QGIS workflow for site-context mapping and proximity analysis. I selected Arch Creek Park from a public Miami-Dade parks dataset, reprojected the relevant park and street layers into EPSG:26917 for meter-based analysis, created a 250 m buffer around the park boundary, clipped nearby streets to that buffer, and designed a finished map layout with appropriate source, CRS, and authorization notes.

The project was designed to show GIS fundamentals that could transfer to drone imagery planning, environmental site review, mapping support, or geospatial technician work.

## Tools Used

- QGIS
- OpenStreetMap XYZ tiles
- Miami-Dade County GIS data
- GeoPackage vector layers

## Files

Suggested project structure:

```text
01_south_florida_qgis_map/
  README.md
  arch_creek_site_context_project.qgz
  data_raw/
  data_processed/
  exports/
    arch_creek_250m_site_context_map_v1.png
    arch_creek_250m_site_context_map_v1.pdf
  screenshots/
  notes/
```

# Raw Data

This folder is used for original source datasets downloaded for the project.

Large raw GIS files are not committed to this repository. The Miami-Dade streets GeoJSON used in this project was excluded because it is over 50 MB and can be re-downloaded from the public Miami-Dade GIS source.

Processed project layers are stored in `data_processed/`.