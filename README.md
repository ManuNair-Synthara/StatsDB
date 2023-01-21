# StatsDB

A simple script to create a database of variables with their dimensions.
 
Given a database, queries can be made for a new dimension and the tool will return its value. 

## How to write the database input

For example, the database in csv format:
```text
Variable,Dim,Value
operations, Op,2
ops_per_packet, Op/pkt,1
watt, J/s,1
speed, Op/s,5
W, =, J/s
```

__Note__: If there are dimension equivalents, those need to be added at the end of the file.
For example, in above code, we are telling the tool that W is equal to J/s

A query can be made to compute Op/s:

```text
db.query("J/Op")
```

It will return:
```text
Value found
Query = 0.2 J/Op
```

Entering a new object into the database can be made simply by:
```text
db.add_var(name, dim, value)
```

Dimensions are to provided as a string. "/"separator when dividing, "." separator when multiplying,

## How does it work?
- Every variable's dimensions are stored in num/den format. 
- Its inverse is also stored. 
- When a query is made, then all possible combinations of the variables are tested.
- If higher powers are to be supported, then those powers and inverse power will need to be stored or at least searched. This is not implemented.
- If there are n entries in the dB, each search costs O(2ˆn).


## Limitations and possible new features
1. The tool currently only supports dimensions of power 1. If higher order dimensions are needed, we have to allow the DB to add inverse as well as higher order powers to the database for each entry. At the moment it only adds a value and its inverse.
2. The tool does not understand dimensions, For example - it does not now that W and J/s are equivalent.
3. If there are multiple variables with the same dimension, it will not work properly. For example, Cx cost is stored as energy and Tx cost is stored as energy. If a new value is queried, it cannot be made only on the basis of a dimension. It will also have to be made in terms of the variable name. It would be good to add this feature.