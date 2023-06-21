"""NDVI Based Change Detector

This script allows the user to read raster layers, calculate change between
two temporal satellite images and visualize the results. The script treats the
3rd band in the raster as red band and 4th band as the near-infrared band (NIR).

This tool accepts the location directory and filenames to GeoTIFF raster files.

This script is best compatible with an environment as configured in 
environment_requirements.yaml shared along with this script.

This file can also be imported as a module and contains the following
functions:

    * load_data() - reads the raster's red and NIR bands into float numpy arrays
    * plt_raster() - visualizes the input numpy array as a map
    * ndvi() - calculates ndvi from the input raster
    * ndvi_change() - calculates loss of vegetation or delta NDVI between the input rasters
"""

# Importing the necessary libraries
import rasterio
import numpy as np
from rasterio.plot import show
import os
import matplotlib.pyplot as plt


def load_data(subdir, filename):
    
    """
    Loads the input raster and returns float type 
    numpy arrays for red and NIR bands in the raster.
    
    Parameters
    ----------
    subdir: str
        Name of the folder within the current directory that contains the data
    filename: str
        Name of the raster file
        
    Returns
    ----------
    tuple:
        First item in the tuple is a numpy array containing the values from the 
        red band of the raster
        
        Second item in the tuple is a numpy array containing the values from the 
        NIR band of the raster
        
    """
    
    # Creating filepaths for the GeoTIFF files from before and after the event
    fp = os.path.join(subdir, filename)
    # Open the raster files in read mode
    raster = rasterio.open(fp)

    # Read bands into numpy arrays and convert the datatype to float
    red = raster.read(3).astype('f4')
    nir = raster.read(4).astype('f4')
    
    return(red,nir)


def plt_raster(band_array):
    
    """
    Parameters
    ----------
    band_array: numpy array (containing float values)
        The input array can be one of the tuple items supplied from the 
        load_data() method
    
    Returns
    ----------
    Plots the numpy array
    
    """
    
    %matplotlib inline
    # Plot the NDVI
    #show(band_array, cmap='terrain')
    # Add colorbar to show the index
    
    plt.imshow(band_array, cmap='terrain_r')
    # Add colorbar to show the index
    plt.colorbar()
    
    return()
  

def ndvi(subdir, filename):
    """
    Reads the input raster using load_data() method and uses its output
    numpy arrays for red and NIR bands to calculate NDVI
    
    Parameters
    ----------
    subdir: str
        Name of the folder within the current directory that contains the data
    filename: str
        Name of the raster file
    
    Returns
    ----------
    numpy array:
        Containing the float NDVI values
    """
    
    np.seterr(divide='ignore', invalid='ignore')
    red, nir = load_data(subdir, filename)
    index = (nir-red)/(nir+red)
    return(index)

def ndvi_change(subdir, fn_before, fn_after):
    """
    Calculates vegetation loss after the event by comparing NDVI from before
    and after the event. Lower values represent the loss. Higher negative 
    values represent a very high loss.
    
    Parameters
    ----------
    subdir: str
        Name of the folder within the current directory that contains the data
    fn_before: str
        Name of the raster file before the event
    fn_after: str
        Name of the raster file after the event
        
    Returns
    ----------
    numpy array:
        Containing NDVI difference between before and after rasters 
    """
    delta = ndvi(subdir,fn_after) - ndvi(subdir,fn_before)
    return(delta)
 
    
    