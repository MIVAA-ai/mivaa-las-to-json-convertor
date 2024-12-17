"""
This class will take file object as input and return a standardize output for las files
"""

import lasio
import lasio.examples
from mappings.LAS2HeaderMappings import HeaderMapping
from utils.DateUtils import DateUtils
from pathlib import Path
from pydantic import ValidationError
from mappings.JSONWellLogFormat import JsonWellLogFormat

class LasScanner:
    def __init__(self, file):
        self._file = file


    def scan(self):
        las_file = lasio.read(self._file, engine="normal", encoding="utf-8")

        # Get different sections of the LAS file in JSON format
        las_headers = self._extract_header(las_file)
        las_curves_headers = self._extract_curve_headers(las_file)
        las_curves_data = self._extract_bulk_data(las_file)
        las_parameters_data = self._extract_parameter_info(las_file)

        # Combine all sections into a single JSON structure
        combined_output = [
            {
                "header": las_headers,
                "parameters": las_parameters_data,
                "curves": las_curves_headers,
                "data": las_curves_data
            }
        ]

        # Validate against the Pydantic model
        try:
            validated_data = JsonWellLogFormat.model_validate(combined_output)
            return validated_data
        except ValidationError as e:
            # Log or handle validation errors
            print("Validation Error:", e)
            raise

    def _extract_bulk_data(self, las_file):
        """
        Extract bulk data (curve measurements) from a LAS file.

        Args:
            las_file (lasio.LASFile): The LAS file object.

        Returns:
            list: A list of data rows, each being an array of values corresponding to the curves.
        """
        # Extract data as a 2D array (rows and columns)
        bulk_data = []

        # Convert LAS curve data into a structured format
        # Use the first curve to determine the number of rows (all curves have the same number of data points)
        num_rows = len(las_file[las_file.curves[0].mnemonic])

        for i in range(num_rows):
            # Create a single row with all curve values for the current index
            row = [las_file[curve.mnemonic][i] for curve in las_file.curves]
            bulk_data.append(row)

        return bulk_data

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

        return header

    def _extract_curve_headers(self, las_file):
        """
        Extract curve information from a LAS file and structure it according to the provided JSON schema.

        Args:
            las_file (lasio.LASFile): The LAS file object.

        Returns:
            list: A list of curves in the specified JSON schema format.
        """
        curves = []

        for curve in las_file.curves:
            # Create a dictionary for each curve based on the schema
            curve_data = {
                "name": curve.mnemonic,  # Curve name or mnemonic
                "description": curve.descr if curve.descr else None,  # Curve description
                "quantity": None,  # LAS files typically don't provide quantity
                "unit": curve.unit if curve.unit else None,  # Unit of measurement
                "valueType": "float",  # Defaulting to float for LAS curve data
                "dimensions": 1,  # LAS curve data is 1D
                "axis": [],  # Axis is typically not defined in LAS
                "maxSize": 20  # Default size
            }
            curves.append(curve_data)

        return curves

    def _extract_parameter_info(self, las_file):
        """
        Extract the parameter information block from a LAS file and structure it into the desired format.

        Args:
            las_file (lasio.LASFile): The LAS file object.

        Returns:
            dict: Parameter information formatted as specified.
        """
        # Initialize the structure for parameter information
        parameter_info = {
            "attributes": ["value", "unit", "description"],
            "objects": {}
        }

        # Loop through the parameters in the LAS file
        for param in las_file.params:
            # Extract parameter mnemonic, unit, value, and description
            mnemonic = param.mnemonic
            unit = param.unit if param.unit else None
            value = param.value
            description = param.descr if param.descr else None

            # Add parameter to the objects section
            parameter_info["objects"][mnemonic] = [value, unit, description]

        return parameter_info