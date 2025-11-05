# PADRÃO CRIACIONAL 2: BUILDER
# objetivo: Separar a construção de um objeto complexo de sua representação final.
# isso nos permite criar diferentes representações do objeto usando o mesmo processo
# de construção.

from models import Employee, Manager, Intern
from exceptions import (
    InvalidEmployeeTypeException, InvalidEmployeeDataException,
    HRSystemException
)

class EmployeeBuilder:
    """
    Esta classe nos ajuda a construir um objeto Employee passo a passo.
    """
    def __init__(self, name, age, email):
        try:
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                raise InvalidEmployeeDataException("Nome não pode ser vazio")
            if not isinstance(age, int) or age <= 0:
                raise InvalidEmployeeDataException(f"Idade deve ser um número inteiro positivo, recebido: {age}")
            if not email or not isinstance(email, str) or len(email.strip()) == 0:
                raise InvalidEmployeeDataException("Email não pode ser vazio")
            
            # Atributos essenciais são passados no início
            self.name = name.strip()
            self.age = age
            self.email = email.strip()
            # Outros atributos começam com valores padrão
            self.department = "Not Assigned"
            self.work_position = "Not Assigned"
            self.salary_per_hour = 0
            self.hire_date = "Not Defined"
            self.emp_type = 1 # 1 para Employee padrão
        except InvalidEmployeeDataException as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao inicializar builder: {str(e)}")

    def set_type(self, emp_type):
        try:
            if not isinstance(emp_type, int):
                raise TypeError(f"Tipo de funcionário deve ser um número inteiro, recebido: {type(emp_type).__name__}")
            if emp_type not in [1, 2, 3]:
                raise InvalidEmployeeTypeException(f"Tipo de funcionário deve ser 1, 2 ou 3, recebido: {emp_type}")
            self.emp_type = emp_type
            return self # Retornar 'self' permite encadear chamadas
        except (TypeError, InvalidEmployeeTypeException) as e:
            raise InvalidEmployeeTypeException(f"Erro ao definir tipo de funcionário: {str(e)}")

    def set_details(self, department, work_position, hire_date):
        try:
            if not department or not isinstance(department, str) or len(department.strip()) == 0:
                raise InvalidEmployeeDataException("Departamento não pode ser vazio")
            if work_position is None:
                work_position = "Not Assigned"
            if hire_date is None:
                hire_date = "Not Defined"
            
            self.department = department.strip()
            self.work_position = str(work_position).strip() if work_position else "Not Assigned"
            self.hire_date = str(hire_date).strip() if hire_date else "Not Defined"
            return self
        except InvalidEmployeeDataException as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao definir detalhes do funcionário: {str(e)}")

    def set_salary(self, salary_per_hour):
        try:
            if not isinstance(salary_per_hour, (int, float)):
                raise TypeError(f"Salário deve ser um número, recebido: {type(salary_per_hour).__name__}")
            if salary_per_hour <= 0:
                raise InvalidEmployeeDataException(f"Salário deve ser um número positivo, recebido: {salary_per_hour}")
            if salary_per_hour > 10000:
                raise InvalidEmployeeDataException(f"Salário por hora não pode exceder R$ 10.000,00, recebido: R$ {salary_per_hour:.2f}")
            self.salary_per_hour = float(salary_per_hour)
            return self
        except (TypeError, InvalidEmployeeDataException) as e:
            raise InvalidEmployeeDataException(f"Erro ao definir salário: {str(e)}")

    def build(self):
        """
        Usa todos os dados fornecidos para construir o objeto final.
        """
        try:
            # Validação final antes de construir
            if self.salary_per_hour <= 0:
                raise InvalidEmployeeDataException(f"Salário deve ser definido antes de construir o funcionário")
            if self.department == "Not Assigned":
                raise InvalidEmployeeDataException("Departamento deve ser definido antes de construir o funcionário")
            
            if self.emp_type == 2:
                return Manager(self.name, self.age, self.email, self.department, self.salary_per_hour, self.hire_date)
            elif self.emp_type == 3:
                return Intern(self.name, self.age, self.email, self.department, self.salary_per_hour, self.hire_date)
            else:
                return Employee(self.name, self.age, self.email, self.department, self.work_position, self.salary_per_hour, self.hire_date)
        except InvalidEmployeeDataException as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao construir funcionário: {str(e)}")