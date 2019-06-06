import h5py
import numpy as np
import os

try:
    os.remove('test1.h5')
except FileNotFoundError:
    pass

try:
    os.remove('test2.h5')
except FileNotFoundError:
    pass

try:
    os.remove('linked_file.h5')
except FileNotFoundError:
    pass

with h5py.File('test1.h5', 'w') as h5file:
    h5file.create_dataset('group1/data1', data=np.arange(1, 5))
    h5file.create_dataset('group1/data2', data=np.arange(4,10))

with h5py.File('test2.h5', 'w') as h5file:
    h5file.create_dataset('group2/data1', data=np.arange(3, 7))
    h5file.create_dataset('group2/data2', data=np.arange(3, 7))
    h5file.create_dataset('group2/data3', data=np.arange(3, 7))
    h5file.create_dataset('group2/data4', data=np.arange(2,12))
    h5file.create_dataset('group2/data5', data=np.arange(2,12))


with h5py.File('linked_file.h5','w') as h5file:
    h5file.create_dataset('non_linked_data/data5', data=np.linspace(0, 4))
    h5file['link1'] = h5py.ExternalLink('test1.h5', '/')
    h5file['link2'] = h5py.ExternalLink('test2.h5', '/')