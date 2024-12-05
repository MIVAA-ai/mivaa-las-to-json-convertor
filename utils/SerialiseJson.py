import json
import numpy as np


class JsonSerializable:
    @staticmethod
    def to_json(obj, **kwargs):
        """
        Converts an object to a JSON string, ensuring all numpy types are serializable.

        Args:
            obj (any): The object to convert and serialize.
            **kwargs: Additional arguments to pass to `json.dumps`.

        Returns:
            str: The JSON string representation of the object.
        """
        def convert(item):
            if isinstance(item, dict):
                return {k: convert(v) for k, v in item.items()}
            elif isinstance(item, list):
                return [convert(v) for v in item]
            elif isinstance(item, np.integer):
                return int(item)
            elif isinstance(item, np.floating):
                return float(item)
            elif isinstance(item, np.ndarray):
                return item.tolist()  # Convert numpy arrays to lists
            else:
                return item  # Return other types unchanged

        serializable_obj = convert(obj)
        return json.dumps(serializable_obj, **kwargs)
