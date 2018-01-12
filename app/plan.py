class users:
    """Proposed extension to the users class so that it can support the plans functionality"""
    def __init__(self):
        self._bankroll = 0
        self._plan = ''

    def get_bankroll(self):
        """bankroll getter method
        :param None
        :returns: the bankroll rounded off to the nearest 2dp """
        return self._bankroll

    def get_plan(self):
        """ the Plan getter method
        :param: None
        :returns: the plan as a string
        """
        return self._plan

    def add_bankroll(self, amount):
        """bankroll setter method
        :param: the amount as a positive integer or float
        :return: the updated amount
        """
        if isinstance(amount, int) or isinstance(amount, float) and amount >= 0:
            self._bankroll += amount
        else:
            raise ValueError("Unexpected value for bankroll")
        return self._bankroll

    def sub_bankroll(self, amount):
        """Bankroll setter method incase we are reducing the bankroll:
        :param: amount as a positive integer or float
        : return the updated bankroll"""
        if isinstance(amount, int) or isinstance(amount, float) and amount >= 0:
            self._bankroll -= amount
        else:
            raise ValueError("Unexpected value for bankroll")
        return self._bankroll

    def set_plan(self, plan):
        """Plan setter method
        :param: a plan as a string
        :returns None , raises a ValueError if the Process failed"""
        plans = ['aon', 'ton', 'don']
        if isinstance(plan, str) and plan in plans:
            self._plan = plan
        else:
            raise ValueError("Unexpected value for plan")


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
