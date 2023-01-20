import csv
import itertools

from .DimVar import DimVar


class StatsDB():
    """
    Database object to record variables
    """
    def __init__(self,
                 csv_fname: str) -> None:
        """
        A database of variables

        Args:
            csv_fname (str): The CSV file that contains the variables
        """
        self.vars = []
        with open(csv_fname) as csvfile:
            reader = csv.DictReader(csvfile)
            for row_idx, row in enumerate(reader):
                self.add_var(str.strip(row['Variable']),
                             str.strip(row['Dim']),
                             float(str.strip(row['Value'])))

    def add_var(self,
                name,
                dim,
                val):
        """
        Adds a new DimVar object to the database

        Args:
            name (str): Name of the variable
            dim (str): Dimensions of the variable. For format check DimVar
            val (float): Value of the variable
        """
        var = DimVar(name,
                     dim,
                     val)
        self.vars.append(var)
        self.vars.append(DimVar.invert(var, var.name+"_inv"))

    def query(self,
              querydim):
        """
        Query the database to compute a particular value with given dimensions

        Args:
            querydim (str): A string denoting the desired dimensions

        Returns:
            DimVar: Dimvar object returned if computable, else None
        """
        queryvar = DimVar("Query",
                          querydim,
                          0)
        # for every product combination of DimVars in dB
        for n in range(len(self.vars)):
            var_tuples = itertools.combinations(self.vars, n)
            for vars in var_tuples:
                # Compute product
                var_prod = DimVar.multiply(vars, "Query")
                # check if resulting dimensions match
                if DimVar.compare_dim(var_prod, queryvar):
                    # if yes, return value
                    print("Value found")
                    var_prod.var_print()
                    return var_prod
        # if no, return False saying expression cannot be computed
        print("Given dims cannot be computed")
        return
