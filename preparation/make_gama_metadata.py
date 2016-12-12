# Make metadata table for GAMA images

from astropy.table import Table
import numpy as np
import warnings
import os
from collections import OrderedDict
import json

# warnings.simplefilter("ignore", RuntimeWarning)


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


for region in ('09', '12', '15'):
    manifest = []
    gama = Table.read('gamazoo{}.csv'.format(region))
    survey = 'gama{}'.format(region)
    N = len(gama)
    t = Table()

    t['coords.0'] = gama['RA']
    t['coords.1'] = gama['DEC']

    #url_stub = "http://gzgama.s3.amazonaws.com/gamazoo{}".format(region)
    url_stub = "http://s3.amazonaws.com/zooniverse-data/project_data/galaxy_zoo/gama{}".format(region)

    loc = [url_stub + '/native/' + x for x in gama['FILENAMENATIVE']]
    t['location.standard'] = loc

    loc = [url_stub + '/invert/' + x for x in gama['FILENAMEINVERT']]
    t['location.inverted'] = loc

    loc = [url_stub + '/thumb/' + x.replace('native-424', 'thumb-150')
           for x in gama['FILENAMENATIVE']]
    t['location.thumbnail'] = loc

    t['metadata.survey'] = survey

    t['metadata.provided_image_id'] = gama['CATAID']

    t['metadata.counters.feature'] = np.zeros(N,dtype=int)
    t['metadata.counters.smooth'] = np.zeros(N,dtype=int)
    t['metadata.counters.star'] = np.zeros(N,dtype=int)

    t['metadata.mag.r'] = gama['PETROAPPMAG']
    t['metadata.mag.abs_r'] = gama['PETROABSMAG']

    t['metadata.petrorad_r'] = gama['PETRORADARCSEC']
    t['metadata.absolute_size'] = gama['PETRORADKPC']

    t['metadata.retire_at'] = 40

    # Write to csv and fits tables
    # ftypes = ('csv','fits')
    # for ft in ftypes:
    #     fname = '../manifests/gama{1}_metadata.{0}'.format(ft, region)
    #     if os.path.isfile(fname):
    #         os.remove(fname)
    #     t.write(fname)

    # Write as json
    for row in t:
        r = OrderedDict()
        r['type'] = 'subject'
        r['group_name'] = survey
        r['group_type'] = 'survey'
        for col in row.colnames:
            r[col] = row[col]
        manifest.append(r)
    fname = '../manifests/{}_manifest.json'.format(survey)
    with open(fname, 'w') as f:
        json.dump(manifest, f, indent=0, separators=(',', ': '))
