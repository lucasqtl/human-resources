# PADRÃO CRIACIONAL 1: FACTORY METHOD (Simple Factory)
# A responsabilidade da Factory é orquestrar a criação, delegando os
# passos da construção para o Builder.

from builders import EmployeeBuilder
from exceptions import (
    InvalidEmployeeTypeException, InvalidEmployeeDataException,
    HRSystemException
)

class EmployeeFactory:
    """
    Esta classe é uma fábrica responsável por criar objetos do tipo Employee.
    """
    @staticmethod
    def create_employee(emp_type, name, age, email, department, work_position, salary, hire_date):
        """
        Usa o EmployeeBuilder para construir o funcionário passo a passo.
        """
        try:
            if emp_type not in [1, 2, 3]:
                raise InvalidEmployeeTypeException(f"Tipo de funcionário deve ser 1, 2 ou 3, recebido: {emp_type}")
            
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                raise InvalidEmployeeDataException("Nome não pode ser vazio")
            
            if not isinstance(age, int) or age <= 0:
                raise InvalidEmployeeDataException(f"Idade deve ser um número inteiro positivo, recebido: {age}")
            
            if not email or not isinstance(email, str) or len(email.strip()) == 0:
                raise InvalidEmployeeDataException("Email não pode ser vazio")
            
            if not department or not isinstance(department, str) or len(department.strip()) == 0:
                raise InvalidEmployeeDataException("Departamento não pode ser vazio")
            
            if not isinstance(salary, (int, float)) or salary <= 0:
                raise InvalidEmployeeDataException(f"Salário deve ser um número positivo, recebido: {salary}")
            
            builder = EmployeeBuilder(name, age, email)
            
            employee = builder.set_type(emp_type) \
                              .set_details(department, work_position, hire_date) \
                              .set_salary(salary) \
                              .build()
            
            return employee
        except (InvalidEmployeeTypeException, InvalidEmployeeDataException) as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao criar funcionário na factory: {str(e)}")