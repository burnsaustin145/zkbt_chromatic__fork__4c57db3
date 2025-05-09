"""
Test the validation of EXTRACT1D extension in FITS files.
"""
import pytest
import os
import numpy as np
from astropy.io import fits

from chromatic.rainbows import Rainbow
from chromatic.rainbows.readers.atoca import from_atoca
from chromatic.rainbows.readers.x1dints import from_x1dints

def test_missing_extract1d_extension_atoca():
    """Test that a ValueError is raised when EXTRACT1D extension is missing in atoca reader."""
    # Create a temporary FITS file without EXTRACT1D extension
    temp_file = "temp_no_extract1d.fits"
    
    # Create a simple FITS file with only PRIMARY HDU
    primary_hdu = fits.PrimaryHDU()
    primary_hdu.header['DATE-OBS'] = '2022-01-01'
    primary_hdu.header['TIME-OBS'] = '00:00:00'
    primary_hdu.header['TFRAME'] = 1.0
    primary_hdu.header['NFRAMES'] = 1
    primary_hdu.header['NGROUPS'] = 1
    primary_hdu.header['NINTS'] = 1
    
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(temp_file, overwrite=True)
    
    # Try to load the file with from_atoca, should raise ValueError
    r = Rainbow()
    with pytest.raises(ValueError, match="No 'EXTRACT1D' extension found"):
        from_atoca(r, temp_file)
    
    # Clean up
    os.remove(temp_file)

def test_missing_extract1d_extension_x1dints():
    """Test that a ValueError is raised when EXTRACT1D extension is missing in x1dints reader."""
    # Create a temporary FITS file without EXTRACT1D extension
    temp_file = "temp_no_extract1d.fits"
    
    # Create a simple FITS file with only PRIMARY HDU
    primary_hdu = fits.PrimaryHDU()
    primary_hdu.header['FILENAME'] = 'jw12345_x1dints.fits'  # Make it look like an x1dints file
    primary_hdu.header['INTSTART'] = 1
    primary_hdu.header['INTEND'] = 1
    primary_hdu.header['INSTRUME'] = 'NIRISS'
    
    hdul = fits.HDUList([primary_hdu])
    hdul.writeto(temp_file, overwrite=True)
    
    # Try to load the file with from_x1dints, should raise ValueError
    r = Rainbow()
    with pytest.raises(ValueError, match="No 'EXTRACT1D' extension found"):
        from_x1dints(r, temp_file)
    
    # Clean up
    os.remove(temp_file)