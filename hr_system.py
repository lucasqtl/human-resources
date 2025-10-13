# PADRÃO CRIACIONAL 3: SINGLETON
# objetivo: Garantir que uma classe tenha apenas uma instância e fornecer um ponto de
# acesso global a essa instância.

from models import Employee, Manager, Intern
from services import Attendance, Compliance

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
        self.employees_list.append(employee)
        self.attendance_list.append(Attendance(employee))
        self.compliance_list.append(Compliance(employee))
        print(f"Number of employees: {len(self.employees_list)}")
        
    def remove_employee(self, index):
        """ Remove um funcionário de todas as listas. """
        if 0 <= index < len(self.employees_list):
            removed = self.employees_list.pop(index)
            self.attendance_list.pop(index)
            self.compliance_list.pop(index)
            Employee.number_of_employees -= 1 
            print(f"{removed.name} has been removed from the system.\n")
        else:
            print("Invalid employee number\n")