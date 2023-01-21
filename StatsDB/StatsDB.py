import csv
import itertools

from .DimVar import DimVar
from .utils import is_list_subset, parse_tags


class StatsDB():
    """
    Database object to record variables
    """
    def __init__(self,
                 csv_fname: str = None) -> None:
        """
        A database of variables

        Args:
            csv_fname (str): The CSV file that contains the variables
        """
        self.variables = []
        self.tags = set()
        self.tags_to_vars_dict = {}
        self.vars_to_tags_dict = {}

        if csv_fname is not None:
            self.parse_csv(csv_fname)

    def parse_csv(self, csv_fname):
        """
        Parses csv files to the db

        Args:
            csv_fname (str): Path to csv file
        """
        with open(csv_fname) as csvfile:
            header = [h.strip() for h in csvfile.readline().split(',')]
            reader = csv.DictReader(csvfile, fieldnames=header)

            for row_idx, row in enumerate(reader):
                new_tags = parse_tags(row["Tags"])
                self.tags = self.tags.union(new_tags)
                new_vars = self.create_var_from_txt(str.strip(row['Name']),
                                                    str.strip(row['Dim']),
                                                    str.strip(row['Value']))
                for tag in new_tags:
                    for new_var in new_vars:
                        self.add_to_db(tag, new_var)

    def add_to_db(self, tag, new_var):
        """
        Updates the dictionaries when adding a new tag and variable

        Args:
            tag (str): New tag
            new_var (DimVar): New variable to be added
        """

        if tag in self.tags_to_vars_dict.keys():
            self.tags_to_vars_dict[tag] += [new_var]
        else:
            self.tags.union(tag)
            self.tags_to_vars_dict[tag] = [new_var]
        if new_var in self.vars_to_tags_dict.keys():
            self.vars_to_tags_dict[new_var] += [tag]
        else:
            self.variables += [new_var]
            self.vars_to_tags_dict[new_var] = [tag]

    def merge_subset(self,
                     db):
        # ToDo
        # for each variable in new dB
        # check if same dims are available in current dB
        # if not, then
        # add variable
        # add tags
        # update tag_to_vars dict
        # update vars_to_tag dict
        pass

    def create_subset(self,
                      tags: list):
        """
        Creates a subset of a dB given tags

        Args:
            tags (list): Tags that we want to use to create a new subset

        Returns:
            StatsDb: A new StatsDb object with only those variables allowed by tag
        """
        new_db = StatsDB()

        # get the variables and update dictionarues
        for tag in tags:
            for var in self.tags_to_vars_dict[tag]:
                new_db.add_to_db(tag, var)
        return new_db

    def create_var_from_txt(self,
                name,
                dim,
                val):
        """
        Creates a new DimVar object to the database given string inputs

        Args:
            name (str): Name of the variable
            dim (str): Dimensions of the variable. For format check DimVar
            val (float): Value of the variable
        """
        if dim == "=":
            # Adding a new dimension equivalent. Ex: W = J/s
            # For each entry in the dB
            for var in self.variables:
                # Check if the right hand side set of variables exist
                partial_match, new_var = DimVar.partial_dim_check(var=var,
                                                                  lhs=name,
                                                                  rhs=val)
                new_vars = self.gen_inverse_var(new_var,
                                          ext="_in_"+name)
        else:
            # When adding new variables
            new_var = DimVar(name,
                             dim,
                             float(val))
            new_vars = self.gen_inverse_var(new_var)
        return new_vars

    def gen_inverse_var(self,
                  new_var,
                  ext: str = "_gen"):
        """
        Adds a new entry and its inverse to the database

        Args:
            new_var (DimVar): New variable to be added to the db
        """
        if new_var is not None:
            gen_var = DimVar.invert(new_var,
                                    new_var.name+ext)
            return [new_var, gen_var]
        return None

    def query(self,
              querydim,
              tags_txt: str = None,
              total: bool = True):

        """
        Query the database to compute a particular value with given dimensions

        Args:
            querydim (str): A string denoting the desired dimensions
            tags_txt (str, optional): Tags as a string. Ex "#CX #RX". Defaults
                                      to None.
            total    (bool, optional): Enables addition of all query results to
                                       a single value. Defaults to True

        Returns:
            DimVar: Dimvar object returned if computable, else None
        """
        queryvar = DimVar("Query",
                          querydim,
                          0)
        if tags_txt is not None:
            tags = parse_tags(tags_txt)
            queryDB = self.create_subset(tags)
        else:
            queryDB = self
        print("="*80)
        print("For query: {} with tag: {}".format(querydim,
                                                  tags_txt))
        print("-"*80)

        result = []
        # for every product combination of DimVars in dB
        for n in range(len(queryDB.variables)+1):
            var_tuples = itertools.combinations(queryDB.variables, n+1)
            for vars in var_tuples:
                # Compute product
                if self.check_for_common_tag(vars): # onlly if vars have shared tags
                    # Only multiply if tags for the variables match
                    var_prod = DimVar.multiply(vars, "Result:")
                    # check if resulting dimensions match
                    if DimVar.compare_dim(var_prod, queryvar):
                        # if yes, return value
                        related_vars = list(vars)
                        # remove variables that come in name, name_gen pairs
                        for var in related_vars:
                            for check_var in related_vars:
                                if check_var.name == var.name+"_gen":
                                    related_vars.remove(var)
                                    related_vars.remove(check_var)

                        print("Related variables:")
                        for v in vars:
                            print("--- Var name: {}, Tag: {}".format(v.name,
                                                                       self.get_tag_string(v)))
                        var_prod.print(prefix="--- ")
                        result += [var_prod]
        if total: # Print accumulated value for the query
            total_val = 0
            for r in result:
                total_val += r.value
            total_var = DimVar("Total",
                               querydim,
                               total_val)
            total_var.print()

        if len(result)==0:
            print("Query gave no results: {} tag: {}".format(querydim,
                                                             tags_txt))
        print("="*80)
        return result

    def check_if_generated(self, var):
        """
        Checks if the var is a generated one for the database, ex - inverse

        Args:
            var (DimVar): variable to be checked

        Returns:
            bool: True if generated, False if not
        """
        if var.name.find("_gen") == -1:
            return False
        else:
            return True

    def print(self):
        """
        Print all variables in the dB

        Args:
            verbosity (str, optional): If min only prints main variables. Defaults to "min".
        """
        print("="*80)
        print("Printing all database variables")
        print("-"*80)
        for var in self.variables:
            # Only print input variables and not generated ones
            if not self.check_if_generated(var):
                var.print()
        print("="*80)

    def write_db_to_csv(self,
                        fname: str):
        """
        Saves the database in CSV format

        Args:
            fname (str): Name of file to save output in
        """
        # print the header
        with open(fname, "w") as csvfile:
            csvfile.write("Name, Dim, Value, Tags \n")
            for var in self.variables:
                if not self.check_if_generated(var):
                    csvfile.write("{}, {}, {}, {} \n".format(var.name,
                                                             DimVar.gen_dimstr(var.nums,
                                                                               var.dens),
                                                                               var.value,
                                                                               self.get_tag_string(var)))
        return

    def get_tag_string(self, var):
        """
        Generates key string for printing to output CSV

        Args:
            var (DimVar): Variable in dB
        """
        keys = list(self.vars_to_tags_dict[var])
        keys_str = "#".join(keys)
        return "#"+keys_str

    def check_for_common_tag(self, vars):
        """
        Checks if there is any common tag between the variables

        Args:
            vars (list): List of variables to check

        Returns:
            bool: True if there is a shared tag, false otherwise
        """
        tag = self.vars_to_tags_dict[vars[0]]
        for var in vars:
            if not is_list_subset(tag, self.vars_to_tags_dict[var]):
                return False
        return True
