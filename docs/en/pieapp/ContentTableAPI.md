# ContentTable API


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

Usage example:
```py
getPlugin(Containers.ContentTable).api("receive", files=files)
```

Or via `getAPI`:
```py
getAPI(Containers.ContentTable, "receive", files=files)
```

Args:
    data (Any): raw data
    struct (dataclass): by default - `pieapp/config.py -> ContentTableStruct`

Returns:
    NoneType

Raises:
    InvalidStructSignature - if data has different structure than `struct`


## Method `transform`
Description:
    Transforms data into raw data types (list or dict) to be transfered into *ffBox API*
    
Raises:
    TransformError - if transform proccess gone wrong
