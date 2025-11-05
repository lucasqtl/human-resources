# commands.py
from abc import ABC, abstractmethod
from models import Employee
from exceptions import (
    InvalidPerformanceLevelException, InvalidIndexException,
    HRSystemException
)

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
        try:
            if employee is None:
                raise ValueError("Funcionário não pode ser None")
            if not isinstance(employee, Employee):
                raise TypeError(f"Objeto deve ser uma instância de Employee, recebido: {type(employee).__name__}")
            if not isinstance(date, str) or len(date.strip()) == 0:
                raise ValueError("Data não pode ser vazia")
            if not isinstance(time, str) or len(time.strip()) == 0:
                raise ValueError("Horário não pode ser vazio")
            if not isinstance(description, str) or len(description.strip()) == 0:
                raise ValueError("Descrição não pode ser vazia")
            
            self._employee = employee
            self._date = date.strip()
            self._time = time.strip()
            self._description = description.strip()
        except (ValueError, TypeError) as e:
            raise HRSystemException(f"Erro ao criar comando de treinamento: {str(e)}")

    def execute(self):
        try:
            self._employee.add_training(self._date, self._time, self._description)
            print(f"Sessão de treinamento '{self._description}' adicionada para {self._employee.name}.")
        except Exception as e:
            raise HRSystemException(f"Erro ao executar comando de adicionar treinamento: {str(e)}")

class AddPerformanceEvaluationCommand(Command):
    def __init__(self, employee: Employee, level: int):
        try:
            if employee is None:
                raise ValueError("Funcionário não pode ser None")
            if not isinstance(employee, Employee):
                raise TypeError(f"Objeto deve ser uma instância de Employee, recebido: {type(employee).__name__}")
            if not isinstance(level, int):
                raise TypeError(f"Nível deve ser um número inteiro, recebido: {type(level).__name__}")
            if level not in [1, 2, 3]:
                raise InvalidPerformanceLevelException(
                    f"Nível de performance deve ser 1 (Good), 2 (Average) ou 3 (Bad), recebido: {level}"
                )
            
            self._employee = employee
            self._level = level
        except (ValueError, TypeError, InvalidPerformanceLevelException) as e:
            raise HRSystemException(f"Erro ao criar comando de avaliação: {str(e)}")

    def execute(self):
        try:
            self._employee.add_performance_evaluation(self._level)
            print(f"Avaliação de performance adicionada para {self._employee.name}.")
        except InvalidPerformanceLevelException as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao executar comando de adicionar avaliação: {str(e)}")

class CommandInvoker:
    def __init__(self, command: Command):
        try:
            if command is None:
                raise ValueError("Comando não pode ser None")
            if not isinstance(command, Command):
                raise TypeError(f"Objeto deve ser uma instância de Command, recebido: {type(command).__name__}")
            self._command = command
        except (ValueError, TypeError) as e:
            raise HRSystemException(f"Erro ao criar invocador de comando: {str(e)}")

    def run(self):
        try:
            self._command.execute()
        except Exception as e:
            raise HRSystemException(f"Erro ao executar comando: {str(e)}")