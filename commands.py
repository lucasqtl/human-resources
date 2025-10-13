# commands.py
from abc import ABC, abstractmethod
from models import Employee

# PADRÃO COMPORTAMENTAL 4: COMMAND
# Objetivo: Encapsular uma solicitação como um objeto, permitindo parametrizar
# clientes com diferentes solicitações, enfileirar ou registrar solicitações e
# suportar operações que podem ser desfeitas.

# Interface do Command
class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

class AddTrainingCommand(Command):
    def __init__(self, employee: Employee, date: str, time: str, description: str):
        self._employee = employee
        self._date = date
        self._time = time
        self._description = description

    def execute(self):
        self._employee.add_training(self._date, self._time, self._description)
        print(f"Sessão de treinamento '{self._description}' adicionada para {self._employee.name}.")

class AddPerformanceEvaluationCommand(Command):
    def __init__(self, employee: Employee, level: int):
        self._employee = employee
        self._level = level

    def execute(self):
        self._employee.add_performance_evaluation(self._level)
        print(f"Avaliação de performance adicionada para {self._employee.name}.")

class CommandInvoker:
    def __init__(self, command: Command):
        self._command = command

    def run(self):
        self._command.execute()