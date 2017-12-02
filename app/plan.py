class Plans(object):
    """the base class that models all the other plans"""

    def __init__(self):
        bank_balance = 0.00

    def get_stake(self):
        """ to be overriden in the different plans"""

    def update_bank_balance(self):
        """Also to be overriden """

    def place_bet(self):
        """
        will be responsible for consolidating all the required functions for
        bet placement, bet settlement and bankroll modification
        """



class TrippleOrNothing(Plans):
    """this plan; you stake all on an odd of three"""

    def __init__(self):
        super().__init__()

    def get_stake(self):
        return self.bank_balance

    def update_bank_balance(self, odds=None):
        pass


class DoubleOrNothing(Plans):
    """ all money back on double odds."""
