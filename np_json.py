''' 
    Wrapper for the json package which reads and writes numpy ndarray's 

    Adapted from Adam Hughes, https://stackoverflow.com/a/27948073, May 2017
'''

import base64
import json
import numpy as np
import quaternion

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        """
        if input object is a ndarray it will be converted into a dict holding dtype, shape and the data base64 encoded
        """
        if isinstance(obj, np.ndarray):
            if obj.dtype == quaternion.quaternion:
                # print(f'converting to float array: {quaternion.as_float_array(obj).tolist()}')
                return dict(__quatarray__=quaternion.as_float_array(obj).tolist())
            return dict(__ndarray__=obj.tolist())
        elif isinstance(obj, quaternion.quaternion):
            return dict(__quaternion__=quaternion.as_float_array(obj))
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def json_numpy_obj_hook(dct):
    """
    Decodes a previously encoded numpy ndarray
    with proper shape and dtype
    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and '__ndarray__' in dct:
        return np.array(dct['__ndarray__']) #, dtype=dct['dtype']).reshape(dct['shape'])
    if isinstance(dct, dict) and '__quatarray__' in dct:
        return quaternion.from_float_array(dct['__quatarray__']) #, dtype=dct['dtype']).reshape(dct['shape'])
    if isinstance(dct, dict) and '__quaternion__' in dct:
        return quaternion.from_float_array(dct['__quaternion__']) #, dtype=dct['dtype']).reshape(dct['shape'])
    return dct

# Overload dump/load to default use this behavior.
def dumps(*args, **kwargs):
    kwargs.setdefault('cls', NumpyEncoder)
    return json.dumps(*args, **kwargs)

def loads(*args, **kwargs):
    kwargs.setdefault('object_hook', json_numpy_obj_hook)    
    return json.loads(*args, **kwargs)

def dump(*args, **kwargs):
    kwargs.setdefault('cls', NumpyEncoder)
    return json.dump(*args, **kwargs)

def load(*args, **kwargs):
    kwargs.setdefault('object_hook', json_numpy_obj_hook)
    return json.load(*args, **kwargs)

if __name__ == '__main__':

    data = np.arange(3, dtype=np.complex)

    one_level = {'level1': data, 'foo':'bar'}
    two_level = {'level2': one_level}

    dumped = dumps(two_level)
    result = loads(dumped)

    print('\noriginal data', data)
    print('\nnested dict of dict complex array', two_level)
    print('\ndecoded nested data', result)