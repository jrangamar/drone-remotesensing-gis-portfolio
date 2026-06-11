# Sand Key Learning Run

## Dataset Information

- Dataset: Sand Key
- Images: 100
- Dataset Size: ~1.1 GB
- Processing Platform: WebODM running in Docker
- Hardware: Apple Mac Mini (M4, 16 GB RAM)
- CRS: WGS 84 / UTM Zone 17N (EPSG:32617)

## Processing Results

- Reconstruction completed successfully.
- Total processing time: 12 minutes 59 seconds.
- Point cloud generated successfully.
- Orthophoto generated successfully.
- Digital Surface Model (DSM) generated successfully.
- Quality report exported.

## GIS Workflow

Imported orthophoto and DSM into QGIS.

Generated:
- Hillshade raster
- Contour lines (0.25 m interval)
- Contour lines (1.0 m interval)

## Observations

- Water produced noticeable reconstruction artifacts.
- Reconstruction edges contain increased noise.
- 0.25 m contours reveal small terrain variations but also amplify reconstruction noise.
- 1.0 m contours indicate that the beach surface is largely flat.
- Hillshade provides a clearer visualization of terrain variation than contours for this dataset.

## Lessons Learned

- Successfully deployed WebODM using Docker.
- Learned WebODM processing workflow.
- Learned relationship between orthophoto, point cloud, DSM, hillshade, and contours.
- Confirmed that CRS information is preserved and automatically recognized by QGIS.
- Demonstrated a complete drone imagery → photogrammetry → GIS workflow.

## Future Improvements

- Process a larger and more topographically varied dataset.
- Compare processing times across datasets.
- Explore point cloud analysis in QGIS or CloudCompare.
- Produce final cartographic layouts from photogrammetry outputs.