# PADRÃO CRIACIONAL 1: FACTORY METHOD (Simple Factory)
# A responsabilidade da Factory é orquestrar a criação, delegando os
# passos da construção para o Builder.

from builders import EmployeeBuilder

class EmployeeFactory:
    """
    Esta classe é uma fábrica responsável por criar objetos do tipo Employee.
    """
    @staticmethod
    def create_employee(emp_type, name, age, email, department, work_position, salary, hire_date):
        """
        Usa o EmployeeBuilder para construir o funcionário passo a passo.
        """
        builder = EmployeeBuilder(name, age, email)
        
        employee = builder.set_type(emp_type) \
                          .set_details(department, work_position, hire_date) \
                          .set_salary(salary) \
                          .build()
        
        return employee