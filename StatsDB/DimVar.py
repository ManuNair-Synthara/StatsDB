def is_list_subset(sublist: list,
                   superlist: list):
    """
    Checks if sublist is a subset of superlist

    Args:
        sublist (list): List to check
        superlist (list): The supposed superset

    Returns:
        bool: True if subset, False if
    """    
    for entry in sublist:
        if entry not in superlist:
            return False

    return True


class DimVar(object):
    """
    Object to store and parse a dimenstion object
    """
    def __init__(self,
                 name: str,
                 dimstr: str,
                 value: float):
        """
        A dimensions object that understands how to operate with dimensions

        Args:
            dims (str): Input dimension strong. Multiply denoted by "."
            and divide by "/"
        """
        self.name = name
        self.value = value
        self.dimstr = dimstr
        self.nums = []
        self.dens = []
        self.dimsstr_parse()
        self.reduce()

    def rename(self,
               name: str):
        """
        To rename the variable

        Args:
            name (str): New name
        """
        self.name = name

    def assign(self,
               value):
        """
        To assign a new value

        Args:
            value (float): new value
        """
        self.value = value

    def dimsstr_parse(self):
        """
        Coverts the provided string into a/b format.
        Each / flips the num and den.
        """
        dimstring = self.dimstr
        dimslist = dimstring.split("/")

        for idx, dims in enumerate(dimslist):
            if idx % 2 == 0:
                self.nums += dims.split(".")
            else:
                self.dens += dims.split(".")
        return

    def print(self):
        """
        Print function for DimVar
        """
        print("{} = {} {}".format(self.name,
                                  self.value,
                                  self.gen_dimstr(self.nums,
                                                  self.dens)))

    def reduce(self):
        """
        Removes those dimensions that are same in numerator and denominator
        """
        for n in self.nums:
            for d in self.dens:
                if n == d:
                    self.nums.remove(n)
                    self.dens.remove(d)
                    break
        return

    @classmethod
    def partial_dim_check(cls,
                          var,
                          lhs: str,
                          rhs: str):
        """
        Checks if the rhs dims are present in the var.
        If it is present, then it returns a DimVar with
        rhs dims replaced by the lhs in var

        Args:
            var (DimVar): Variable that we want to check
            lhs (str): The new dimension. Ex: W
            rhs (str): The dimension to be added if lhs exists

        Returns:
            bool, Dimvar: True if partial match, new DimVar with replaced dims
        """
        # Create a new variable placeholder to help clean up the input string format
        rhs_var = DimVar("rhs_var", rhs, 0)
        # check if new_var nums/dens is a subset of var nums/dens
        nums_check = is_list_subset(rhs_var.nums, var.nums)
        dens_check = is_list_subset(rhs_var.dens, var.dens)
        partial_match = nums_check and dens_check
        if partial_match:
            # Create a new value to return, first only add the new dim
            lhs_var = DimVar(var.name, lhs, var.value)
            # Now add the remaining dims
            lhs_var.nums += [n for n in var.nums if n not in rhs_var.nums]
            lhs_var.dens += [d for d in var.dens if d not in rhs_var.dens]

            return partial_match, lhs_var
        return partial_match, None


    @classmethod
    def compare_dim(cls,
                    var1,
                    var2):
        """
        Compares if dimensions of two DimVars match

        Args:
            var1 (DimVar): Var to compare
            var2 (DimVar): Var to compate

        Returns:
            Bool: True if matches, false if not
        """
        a_num_set = sorted(var1.nums)
        a_den_set = sorted(var1.dens)
        b_num_set = sorted(var2.nums)
        b_den_set = sorted(var2.dens)

        if (a_num_set == b_num_set) and (a_den_set == b_den_set):
            return True
        else:
            return False

    @classmethod
    def gen_dimstr(cls,
                   nums,
                   dens):
        """
        Generates a dimstring that can be used to create a new DimVar object

        Args:
            nums (List of string): For the numerator
            dens (List of strings): For the denominator

        Returns:
            str: Can be used to create a new object
        """
        return ".".join(nums) + "/" + ".".join(dens)

    @classmethod
    def multiply(cls,
                 vars,
                 name: str):
        """
        Multipliers an iterable of DimVars

        Args:
            vars (iterable): An iterable that generates DimVar objects
            name (str): For the product

        Returns:
            DimVar: Product of all values generated by the input iterable
        """
        nums = []
        dens = []
        val = 1
        for v in vars:
            nums += v.nums
            dens += v.dens
            val *= v.value
        dimstr = cls.gen_dimstr(nums, dens)
        result = DimVar(name, dimstr, val)
        return result

    @classmethod
    def invert(cls,
               var,
               name: str):
        """
        Inverts a DimVar object

        Args:
            var (DimVar): A DimVar variable
            name (str): Name for the inverted variable

        Returns:
            DimVar: Inverse of the input
        """
        dens = var.nums
        nums = var.dens
        dimstr = cls.gen_dimstr(nums, dens)
        var3 = DimVar(name, dimstr, 1 / var.value)
        return var3
