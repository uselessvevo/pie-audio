# ContentTable API


## Method `mount`
Description:
    Sets file structure, columns count, titles, default alignment and stretch

Returns:
    NoneType


## Method `set_structure/setStructure`
Description:
    Receive overrides default structure
    
Args:
    struct (dataclass): dataclass structure
    
Returns:
    NoneType
    
Raises:
    TypeError - if structure is not dataclass based


## Method `receive`
Description:
    Receive data from the source (for example, list of files) and parse it into dataclass structure

Args:
    files (list[str]): list of input files

Returns:
    NoneType


## Method `transform`
Description:
    Transforms data into raw data types (list or dict) to be transfered into *ffBox API*
    
Raises:
    TransformError - if transform proccess gone wrong
