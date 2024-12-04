"""
This class will take file object as input and return a standardize output for las files
"""

import lasio
import lasio.examples
from mappings.LAS2HeaderMappings import HeaderMapping
from utils.DateUtils import DateUtils
from pathlib import Path

class LasScanner:
    def __init__(self, file):
        self._file = file


    def scan(self):
        las_file = lasio.read(self._file)

        #getting the different section of las file in json format
        las_headers = self._extract_header(las_file)


    #extracting only the headers of the well log file
    def _extract_header(self, las_file):
        #getting the default mapping for the well logs header
        header_mapping = HeaderMapping.get_default_mapping()

        # Build header information based on mapping
        header = {}

        for key, las_fields in header_mapping.items():
            # Handle fields that map to multiple LAS attributes
            header[key] = None
            for las_field in las_fields:
                value = las_file.well[las_field].value if las_field in las_file.well else None

                if value is not None:
                    header[key] = value
                    break  # Stop at the first non-None value

            # Apply ISO 8601 conversion for date fields
            if key in HeaderMapping.get_date_fields() and header[key] is not None:
                header[key] = DateUtils.to_iso8601(header[key])

            # Add any remaining LAS file headers not included in the mapping
            for las_field in las_file.well.keys():
                if las_field not in {field for fields in header_mapping.values() for field in fields}:
                    header[las_field] = las_file.well[las_field].value

            # Putting the name of well log file
            if key in 'name':
                header[key] = Path(self._file).stem

        print(header)