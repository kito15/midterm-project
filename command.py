class Command:
    def execute(self):
        raise NotImplementedError

class AddCommand(Command):
    def __init__(self, facade, num1, num2):
        self.facade = facade
        self.num1 = num1
        self.num2 = num2
        self.result = None

    def execute(self):
        self.result = self.num1 + self.num2
        self.facade.add_record('add', self.num1, self.num2, self.result)
        return self.result

class SubtractCommand(Command):
    def __init__(self, facade, num1, num2):
        self.facade = facade
        self.num1 = num1
        self.num2 = num2
        self.result = None

    def execute(self):
        self.result = self.num1 - self.num2
        self.facade.add_record('subtract', self.num1, self.num2, self.result)
        return self.result

class MultiplyCommand(Command):
    def __init__(self, facade, num1, num2):
        self.facade = facade
        self.num1 = num1
        self.num2 = num2
        self.result = None

    def execute(self):
        self.result = self.num1 * self.num2
        self.facade.add_record('multiply', self.num1, self.num2, self.result)
        return self.result

class DivideCommand(Command):
    def __init__(self, facade, num1, num2):
        self.facade = facade
        self.num1 = num1
        self.num2 = num2
        self.result = None

    def execute(self):
        if self.num2 == 0:
            return "Error: Division by zero"
        self.result = self.num1 / self.num2
        self.facade.add_record('divide', self.num1, self.num2, self.result)
        return self.result

class SaveHistoryCommand(Command):
    def __init__(self, facade, filename):
        self.facade = facade
        self.filename = filename

    def execute(self):
        return self.facade.save_to_csv(self.filename)

class LoadHistoryCommand(Command):
    def __init__(self, facade, filename):
        self.facade = facade
        self.filename = filename

    def execute(self):
        return self.facade.load_from_csv(self.filename)

class ViewHistoryCommand(Command):
    def __init__(self, facade):
        self.facade = facade

    def execute(self):
        return self.facade.view_data()

class ClearHistoryCommand(Command):
    def __init__(self, facade):
        self.facade = facade

    def execute(self):
        return self.facade.clear_data()
