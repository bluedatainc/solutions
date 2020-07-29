## NYC Taxi MLOps Example

Versions of the Jupyter notebook are provided for both Kubernetes and Epic.

For XGBoost:
- A truncated dataset (demodata.zip) is provided within the "Taxi Datasets" folder, please unzip it before running the demo.

Datasets:
- demodata.zip (for the XGBoost demo) contains a sample of approximately 375,000 NYC taxi rides from January-June 2019. Pickup and dropoff locations are specified as location ID numbers (lookup-ipyheader.csv contains the appropriate mappings).
- lookup-ipyheader is a lookup table between location ID numbers and the longitude/latitude coordinates.
The two datasets above are merged within the Jupyter notebook code.
