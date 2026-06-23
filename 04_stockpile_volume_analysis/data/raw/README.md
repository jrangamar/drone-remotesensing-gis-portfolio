

# Raw data

The raw source files for this project come from the public **Stockpiles** sample dataset published by Virtual Surveyor.

Dataset page:
https://support.virtual-surveyor.com/support/solutions/articles/1000310553-download-sample-datasets#Stockpiles

Virtual Surveyor describes the dataset as a drone-data example for stockpile inventory workflows and lists GeoID as the data provider.

## Expected local placement

```text
data/raw/virtual_surveyor_stockpiles/Stockpiles/
```

Principal inputs:

```text
Zeebrugge Stocks.Ii.tif   # Orthophoto / RGB imagery
Zeebrugge Stocks.Ei.tif   # Elevation raster / DSM
```

The supplied perimeter data was also imported into QGIS for the boundary-sensitivity comparison.

## Repository policy

The large downloaded source files should remain local and should not be committed to Git unless their redistribution terms and repository-size implications have been reviewed.

This file preserves the source URL, expected directory structure, and key filenames so the public sample dataset can be reacquired later.