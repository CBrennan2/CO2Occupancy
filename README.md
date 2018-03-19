# CO2Occupancy

### Summary
This repository contains an experiment dataset for Wireless Sensor Network (WSN)-based room occupancy estimation. The tests included are from observation of control settings with known true occupancy levels. 
The included script provides basic functionality, loading the dataset into pandas dataframe format and plotting the data series against their corresponding occupancy labels (Tested w. Python 3.5.3).

The objective of this dataset is to facilitate the design and assessment of *learned* occupancy estimation models which perform without knowledge of the mass-balance parameters of the deployed environment.

### Acquisition
A wireless sensing prototype was constructed in order to observe the deployment environment and generate a data series to train occupancy estimation. The main sensing capability was provided by:
- [DHT22 Sensor](https://learn.adafruit.com/dht/overview)
- [K30 CO2 Sensor](https://www.co2meter.com/products/k-30-co2-sensor-module)

Temperature, Humidity, and CO2 concentration were each read at 0.33Hz. To address the noise in concentration readings, the median of this data was taken on a per-minute basis.

2-3 sensoring nodes were deployed in a conference room with dimensions: 5.8x5.35x2.8m^3. Data is partitioned by date of acqusition and all present sensor streams are grouped in the same directory.