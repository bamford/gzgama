# Make metadata table for GAMA images

from astropy.table import Table
import numpy as np
import warnings
import os

warnings.simplefilter("ignore", RuntimeWarning)

for region in ('09', '12', '15'):

    gama = Table.read('gamazoo{}.csv'.format(region))

    N = len(gama)

    t = Table()

    t['coords.0'] = gama['RA']
    t['coords.1'] = gama['DEC']

    url_stub = "http://gzgama.s3.amazonaws.com/gamazoo{}".format(region)

    loc = [url_stub + '/native/' + x for x in gama['FILENAMENATIVE']]
    t['location.standard'] = loc

    loc = [url_stub + '/invert/' + x for x in gama['FILENAMEINVERT']]
    t['location.inverted'] = loc

    loc = [url_stub + '/thumb/' + x.replace('native-424', 'thumb-150')
           for x in gama['FILENAMENATIVE']]
    t['location.thumbnail'] = loc

    t['survey'] = gama['SURVEY']

    t['metadata.provided_image_id'] = gama['CATAID']

    t['metadata.counters.feature'] = np.zeros(N,dtype=int)
    t['metadata.counters.smooth'] = np.zeros(N,dtype=int)
    t['metadata.counters.star'] = np.zeros(N,dtype=int)

    t['metadata.mag.r'] = gama['PETROAPPMAG']
    t['metadata.mag.abs_r'] = gama['PETROABSMAG']

    t['metadata.petrorad_r'] = gama['PETRORADARCSEC']
    t['metadata.absolute_size'] = gama['PETRORADKPC']

    t['metadata.gama_region'] = '{}'.format(region)

    t['metadata.retire_at'] = 40

    # Write to table
    ftypes = ('csv','fits')
    for ft in ftypes:
        fname = '../manifests/gama{1}_metadata.{0}'.format(ft, region)
        if os.path.isfile(fname):
            os.remove(fname)
        t.write(fname)
