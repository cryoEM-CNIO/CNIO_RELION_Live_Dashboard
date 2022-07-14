# README

This script provides LIVE feedback for On-The-Fly data processing with RELION 

## Installation

### Creating conda environment (or updating your python setup)
We encourage you to create a relion_dashboard conda environment that you can use to run this script and others from our repositories (CNIO_RELION_Live_Dashboard & CNIO_RELION_Analyse_Dashboard)

```
conda create -n relion_dashboard python=3.8
conda activate relion_dashboard
pip install pandas dash=="2.3.1" starfile pathlib2 numpy glob2 pathlib argparse seaborn sklearn regex dash-cytoscape
```

### Clone CNIO_RELION_Live_Dashboard
`git clone https://github.com/cryoEM-CNIO/CNIO_RELION_Live_Dashboard`

## Usage
### Run the script from your project directory

Execute the script from your project directory
`relion_live.py`

If the script is not in your PATH, use the full explicit path to the script.

It admits two arguments (quite often the default parameters are ok):
* **--port**: choose the port were you want to launch the webapp (default: 8051)
* **--host**: choose the IP address where you want the webapp to be hosted (default: localhost).

Example:
`relion_live.py --host 01.010.101.010 --port 805`

Open a web browser and access the server (localhost:8050)

## Displaying images for micrograph and CTF

In order for this to work, you need to create png files for every image and ctf in the motioncorr and ctffind folders, next to mrc/ctf files and with the same name.

To do this we use an external job type from the relion GUI to run **png\_out.py**

If you want to include it in your relion\_it.py schedule use the Schemes folder in this repository.
