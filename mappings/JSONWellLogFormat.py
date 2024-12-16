from typing import List, Dict, Union, Optional
from pydantic import BaseModel, Field, RootModel, ConfigDict

# Represents the top-level structure for parameters
class Parameters(BaseModel):
    attributes: List[str] = Field(..., title="List of attribute names")
    objects: Dict[str, List[Union[str, float, None]]] = Field(
        ..., title="Dictionary of objects, each with an array of values"
    )

class Axis(BaseModel):
    title: Optional[str] = Field(None, title="Axis")

class Curve(BaseModel):
    name: str = Field(..., title="Curve name or mnemonic")
    description: Optional[str] = Field(None, title="Curve description")
    quantity: Optional[str] = Field(None, title="Quantity")
    unit: Optional[str] = Field(None, title="Unit of measurement")
    valueType: Optional[str] = Field(
        "float",
        title="Value type",
        enum=["float", "integer", "string", "datetime", "boolean", None],
    )
    dimensions: int = Field(1, title="Number of dimensions", ge=1)
    axis: Optional[List[Axis]] = Field(None, title="Axis specification of dimensions")
    maxSize: int = Field(20, title="Maximum storage size for string data", ge=0)

class Header(BaseModel):
    name: str = Field(..., title="Log name")
    description: Optional[str] = Field(None, title="Log description")
    well: Optional[str] = Field(None, title="Well name")
    wellbore: Optional[str] = Field(None, title="Wellbore name")
    field: Optional[str] = Field(None, title="Field name")
    country: Optional[str] = Field(None, title="Country of operation")
    date: Optional[str] = Field(None, title="Logging date")
    operator: str = Field(None, title="Operator company name")
    serviceCompany: Optional[str] = Field(None, title="The Service company name")
    runNumber: Optional[str] = Field(None, title="Run number")
    elevation: Optional[float] = Field(None, title="Vertical distance between measured depth 0.0 and mean sea level")
    source: Optional[str] = Field(None, title="Source system of process of this log")
    startIndex: Optional[float] = Field(None, title="Value of the first index")
    endIndex: Optional[float] = Field(None, title="Value of the last index")
    step: Optional[float] = Field(None, title="Distance between indices if regularly sampled")
    dataUri: Optional[str] = Field(None, title="Point to data source in case this is kept separate")

    # Use ConfigDict for configuration
    model_config = ConfigDict(extra='allow')  # Allow additional attributes

class DataRow(RootModel[List[Union[str, float, bool, None, List[Union[str, float, bool, None]]]]]):
    """Represents a single row of data as a root model."""

class Logs(BaseModel):
    header: Header  # A detailed well log header as per your Header model
    parameters: Parameters = Field(..., title="Parameters representing metadata sections")
    curves: List[Curve] = Field(..., title="Curves in the log")
    data: List[DataRow] = Field(..., title="Data rows representing the curve data")


class JsonWellLogFormat(RootModel[List[Logs]]):
    """Root model for JSON Well Log Format."""