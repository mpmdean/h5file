import h5py
import re


class h5file:
    """Container for h5file providing easier access to see the keys
    and loading based on partially matched keys
    """
    def __init__(self, filename):
        """Class initialization
        
        Paramters
        ---------
        filename : string
            path to h5 file.
        """
        f = h5py.File(filename, 'r')
        self.filename = filename
        self.f = f


    def populate_keys(self):
        """Get the full set of keys in the h5file"""
        all_keys = []
        path_list = []
        def walk_groups(group):
            for key, obj in group.items():
                if isinstance(obj, h5py.Dataset):
                    all_keys.append("/".join(path_list + [key]))
                else:
                    if obj is not None:
                        path_list.append(key)
                        walk_groups(obj)
                        path_list.pop()
            return
        
        walk_groups(self.f)
        self.all_keys = all_keys


    def keys(self, getkey=''):
        """Find all keys that match the requested key
        
        Parameters
        ----------
        getkey : string
            key pattern to search for
            regular expressions 
            https://docs.python.org/3/library/re.html
            The default of '.' matches all keys.
            
        Returns
        -------
        matching_keys : list of key string
            The keys that match what is requested.
        """
        if hasattr(self, 'all_keys') is False:
            self.populate_keys()

        if getkey == '':
            matching_keys = self.all_keys
        else:
            matching_keys = [key for key in self.all_keys
                             if re.search(getkey, key)]

        return matching_keys


    def index(self, getkey):
        """
        Try to return the dataset associated with a key.
        Errors are thrown in the key matched none or more than
        one dataset

        Parameters
        ----------
        getkey : string
            key pattern to search for
            regular expressions 
            https://docs.python.org/3/library/re.html
            
        Returns
        -------
        ds : h5py dataset
            The dataset associated with the key
            use ds[()] to extract the data."""
        try:
            return self.f[getkey]
        except KeyError:
            pass
        matching_keys = self.keys(getkey=getkey)
        if len(matching_keys) == 1:
            return self.f[matching_keys[0]]
        elif len(matching_keys) > 1:
            raise Exception("{} matches found: {}".format(len(matching_keys),
                                                         matching_keys))
        elif len(matching_keys) == 0:
            raise Exception("{} not found".format(key))


    def items(self, getkey=''):
        """
        Return list of (key, dataset) pairs where the key
        matches getkey
        
        Parameters
        ----------
        getkey : string
            key pattern to search for
            regular expressions 
            https://docs.python.org/3/library/re.html
            The default of '.' matches all keys.
            
        Returns
        -------
        list_of_items : list
            (key, dataset) pairs where the key matches getkey
        """   
        list_of_items = [(key, self.f[key]) for key in self.keys(getkey)]
        return list_of_items
        

    def get_description(self):
        """Make a string describing the file and its keys.
        
        Returns
        ----------
        description : string
                description
        """
        description = 'Filename is: {} \nKeys are:\n'.format(self.filename)
        description += "\n".join(self.keys()) + '\n'
        return description


    def __str__(self):
        """Show description."""
        return self.get_description()


    def __repr__(self):
        """Show description."""
        return self.get_description()


    def _ipython_key_completions_(self):
        """Enable tab completion when indexing keys."""
        if hasattr(self, 'all_keys') is False:
            self.populate_keys()
        return self.all_keys
        
    
    def __getitem__(self, key):
        """Associate [] with indexing."""
        return self.index(key)


    def _ipython_key_completions_(self):
        """Tab completions for key."""
        if hasattr(self, 'all_keys') is False:
            self.populate_keys()
        return self.all_keys
    
