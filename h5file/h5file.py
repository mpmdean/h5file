import h5py

class h5file:
    """Container for h5file providing views of the keys and loading
    based on partially matched keys
    """
    def __init__(self, filename):
        """Class initialization
        
        Paramters
        ---------
        filename : string
            path to h5 file.
        """
        f = h5py.File(filename, 'r')

        keys = []
        path = []
        def walk_groups(group):
            for key, obj in group.items():
                if isinstance(obj, h5py.Dataset):
                    keys.append("/".join(path + [key]))
                else:
                    path.append(key)
                    walk_groups(obj)
                    path.pop()
            return
        
        walk_groups(f)

        self.filename = filename
        self.f = f
        self.keys = keys

        
    def matchkeys(self, getkey):
        """Find all keys that match the requested key
        
        Parameters
        ----------
        getkey : string
            key pattern to search for
            
        Returns
        -------
        matching_keys : list of key string
            The keys that match what is requested.
        """
        return [key for key in self.keys if getkey in key]

    
    def index(self, key):
        """
        Try to return the dataset associated with a key.
        Errors are thrown in the key matched none or more than
        one dataset

        Parameters
        ----------
        key : string
            key to search for
            
        Returns
        -------
        ds : h5py dataset
            The dataset associated with the key
            use ds[()] to extract the data."""
        matching_keys = self.matchkeys(key)
        if len(matching_keys) == 1:
            return self.f[matching_keys[0]]
        elif len(matching_keys) > 1:
            raise Exception("{} matches found: {}".format(len(matching_keys),
                                                         matching_keys))
        elif len(matching_keys) == 0:
            raise Exception("{} not found".format(key))


    def get_description(self):
        """Make a string describing the file and its keys.
        
        Returns
        ----------
        description : string
                description
        """
        description = 'Filename is: {} \nKeys are:\n'.format(self.filename)
        description += "\n".join(self.keys) + '\n'
        return description
 
    def __str__(self):
        """Show description."""
        return self.get_description()

    def __repr__(self):
        """Show description."""
        return self.get_description()
    
    def __getitem__(self, key):
        """Associate [] with indexing."""
        return self.index(key)
    
