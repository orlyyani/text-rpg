class Gold:
    def __init__(self, amount=0):
        self.amount = amount

    def add_gold(self, amount):
        self.amount += amount

    def get_gold(self):
        return self.amount

    def __str__(self):
        return f'{self.amount} gold'