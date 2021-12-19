# README

This script provides LIVE feedback for On-The-Fly data collection with RELION (very useful to explore already processed datasets too!)

## Creating conda environment that works

`conda create -n relion_dashboard python=3`  
`conda activate relion_dashboard`  
`pip install pandas`  
`pip install dash`  
`pip install "starfile=0.4.10"`  
`pip install pathlib2`  
`conda deactivate`

Download relion\_it.py and put in your path

## Run the script

`conda activate relion_dashboard`  
**`relion_live.py`**

Open a web browser and access the server (localhost:8050) - _you can edit the script and change localhost for full IP address in order to access form another computer in the network_

## Display images for micrograph and ctf

In order for this to work, you need to create png files for every image and ctf in the motioncorr and ctffind folders.

To do this we use an external job from the relion GUI to run **png\_out.py** so you can include it in your relion\_it.py schedule (include folder+job.star and modify scheme.star).
