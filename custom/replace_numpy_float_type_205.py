import numpy as np


@custom
def replace_numpy_float_type(*args, **kwargs):
    """
    Recursively replace deprecated numpy float types with np.float64 to ensure compatibility with numpy 2.0.
    """

    data: dict = None

    def _replace(obj):
        if isinstance(obj, dict):
            return {k: _replace(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_replace(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(_replace(item) for item in obj)
        elif isinstance(obj, (np.float64, np.float16, np.float32, np.floating)):
            # Replace np.float_ with np.float64
            return np.float64(obj)
        else:
            return obj

    return _replace(data)
