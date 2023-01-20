# StatsDB

A simple script to create a database of variables with their dimensions.
 
Given a database, queries can be made for a new dimension and the tool will return its value. 

For example, the database in csv format:
```text
Variable,Dim,Value
operations, Op,2
ops_per_packet, Op/pkt,1
watt, J/s,1
speed, Op/s,5
```

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
