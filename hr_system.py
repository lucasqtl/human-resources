# PADRÃO CRIACIONAL 3: SINGLETON
# objetivo: Garantir que uma classe tenha apenas uma instância e fornecer um ponto de
# acesso global a essa instância.

from models import Employee, Manager, Intern
from services import Attendance, Compliance
from exceptions import (
    InvalidEmployeeIndexException, ListSynchronizationException,
    HRSystemException
)

class HRSystem:
    """
    Esta é a classe Singleton que gerencia o estado de todo o sistema de RH.
    """
    _instance = None 

    @staticmethod
    def get_instance():
        """
        Método estático que atua como o ponto de acesso global.
        Cria a instância se ela não existir e a retorna.
        """
        if HRSystem._instance is None:
            HRSystem._instance = HRSystem()
        return HRSystem._instance

    def __init__(self):
        """
        O construtor só deve ser executado uma vez.
        """
        if hasattr(self, '_initialized'):
            return
        
        self.employees_list = []
        self.attendance_list = []
        self.compliance_list = []
        self._initialized = True
        
    def add_employee(self, employee):
        """ Adiciona um funcionário e seus serviços correspondentes às listas. """
        try:
            if employee is None:
                raise ValueError("Funcionário não pode ser None")
            if not isinstance(employee, Employee):
                raise TypeError(f"Objeto deve ser uma instância de Employee, recebido: {type(employee).__name__}")
            
            self.employees_list.append(employee)
            
            try:
                attendance = Attendance(employee)
                self.attendance_list.append(attendance)
            except Exception as e:
                # Rollback: remove o funcionário se falhar ao criar attendance
                self.employees_list.pop()
                raise HRSystemException(f"Erro ao criar registro de frequência: {str(e)}")
            
            try:
                compliance = Compliance(employee)
                self.compliance_list.append(compliance)
            except Exception as e:
                # Rollback: remove funcionário e attendance se falhar ao criar compliance
                self.employees_list.pop()
                self.attendance_list.pop()
                raise HRSystemException(f"Erro ao criar registro de compliance: {str(e)}")
            
            # Verifica sincronização das listas
            if not (len(self.employees_list) == len(self.attendance_list) == len(self.compliance_list)):
                raise ListSynchronizationException(
                    f"Listas dessincronizadas após adicionar funcionário. "
                    f"Funcionários: {len(self.employees_list)}, "
                    f"Frequência: {len(self.attendance_list)}, "
                    f"Compliance: {len(self.compliance_list)}"
                )
            
            print(f"Number of employees: {len(self.employees_list)}")
        except (ValueError, TypeError, ListSynchronizationException) as e:
            raise HRSystemException(f"Erro ao adicionar funcionário: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro inesperado ao adicionar funcionário: {str(e)}")
        
    def remove_employee(self, index):
        """ Remove um funcionário de todas as listas. """
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidEmployeeIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if len(self.employees_list) == 0:
                raise InvalidEmployeeIndexException("Não há funcionários para remover")
            if index >= len(self.employees_list):
                raise InvalidEmployeeIndexException(
                    f"Índice {index} está fora do range. Total de funcionários: {len(self.employees_list)}"
                )
            
            # Verifica sincronização antes de remover
            if not (len(self.employees_list) == len(self.attendance_list) == len(self.compliance_list)):
                raise ListSynchronizationException(
                    f"Listas dessincronizadas antes de remover funcionário. "
                    f"Funcionários: {len(self.employees_list)}, "
                    f"Frequência: {len(self.attendance_list)}, "
                    f"Compliance: {len(self.compliance_list)}"
                )
            
            removed = self.employees_list.pop(index)
            
            try:
                self.attendance_list.pop(index)
            except IndexError:
                raise ListSynchronizationException(
                    f"Erro ao remover registro de frequência no índice {index}. "
                    f"Lista de frequência tem apenas {len(self.attendance_list)} elementos"
                )
            
            try:
                self.compliance_list.pop(index)
            except IndexError:
                raise ListSynchronizationException(
                    f"Erro ao remover registro de compliance no índice {index}. "
                    f"Lista de compliance tem apenas {len(self.compliance_list)} elementos"
                )
            
            Employee.number_of_employees -= 1
            
            # Verifica sincronização após remover
            if not (len(self.employees_list) == len(self.attendance_list) == len(self.compliance_list)):
                raise ListSynchronizationException(
                    f"Listas dessincronizadas após remover funcionário. "
                    f"Funcionários: {len(self.employees_list)}, "
                    f"Frequência: {len(self.attendance_list)}, "
                    f"Compliance: {len(self.compliance_list)}"
                )
            
            print(f"{removed.name} has been removed from the system.\n")
        except (TypeError, InvalidEmployeeIndexException, ListSynchronizationException, IndexError) as e:
            raise InvalidEmployeeIndexException(f"Erro ao remover funcionário: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro inesperado ao remover funcionário: {str(e)}")