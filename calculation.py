class Calculation:

    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2

    def __validate(self):
        if not self.number1:
            return "Number 1 not present!"
        elif not self.number2:
            return "Number 2 not present!"
        elif self.number2 == 0:
            return "Number 2 can not be 0 - division by 0 not possible"
        else:
            return self

    def calculate(self):
        if isinstance(self.__validate(), Calculation):
            return CalculationResult(self.number1 + self.number2,
                                     self.number1 - self.number2,
                                     self.number1 * self.number2,
                                     self.number1 / self.number2)
        else:
            return self.__validate()


class CalculationResult:
    def __init__(self, sum, diff, product, quotient):
        self.sum = sum
        self.diff = diff
        self.product = product
        self.quotient = quotient

    def return_as_json(self):
        return {
            'sum': self.sum,
            'diff': self.diff,
            'product': self.product,
            'quotient': self.quotient
        }