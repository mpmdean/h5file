# h5file
Wrapper for h5py allowing lazy indexing and straightfoward discovery of the keys.  

This is conveneint for exploring files in the usual case where the number of different datasets isn't too large. This is especially convenient when the h5 file contains links, which aren't fully explored by the default ```h5py.visit``` and ```h5py.visititems``` methods. 

```
from h5file import h5file
h = hfile('linked_file.h5')
```

Calling ```h``` or ```print(h)``` will show the files and keys.

Indexing returns datasets including partial matches string (provided they only match one key).  Do

```
hdfdataset = h['data1']
```

or 
```
data = h['data1'][()]
```

To get the data. The search function supports [regular expressions](https://docs.python.org/3/library/re.html).