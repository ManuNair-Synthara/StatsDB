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
            header = [h.strip() for h in csvfile.readline().split(',')]
            reader = csv.DictReader(csvfile, fieldnames=header)
            for row_idx, row in enumerate(reader):
                self.add_var(str.strip(row['Variable']),
                             str.strip(row['Dim']),
                             str.strip(row['Value']))

    def print(self):
        """
        Print all variables in the dB

        Args:
            verbosity (str, optional): If min only prints main variables. Defaults to "min".
        """        
        print("="*80)
        print("Printing all database variables")
        print("-"*80)
        for var in self.vars:
            # Only print variables and not their inverses
            var.print()
        print("="*80)

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
        if dim == "=":
            # Adding a new dimension equivalent. Ex: W = J/s
            # For each entry in the dB
            for var in self.vars:
                # Check if the right hand side set of variables exist
                partial_match, renamed_var = DimVar.partial_dim_check(var=var,
                                                                      lhs=name,
                                                                      rhs=val)
                if renamed_var is not None:
                    self.vars.append(renamed_var)
                    self.vars.append(DimVar.invert(renamed_var,
                                                   renamed_var.name+"_inv"))

        else:
            # When adding new variables
            var = DimVar(name,
                         dim,
                         float(val))
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
                var_prod = DimVar.multiply(vars, "Query result")
                # check if resulting dimensions match
                if DimVar.compare_dim(var_prod, queryvar):
                    # if yes, return value
                    var_prod.print()
                    return var_prod
        # if no, return False saying expression cannot be computed
        print("Given dims cannot be computed")
        return
