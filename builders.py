# PADRÃO CRIACIONAL 2: BUILDER
# objetivo: Separar a construção de um objeto complexo de sua representação final.
# isso nos permite criar diferentes representações do objeto usando o mesmo processo
# de construção.

from models import Employee, Manager, Intern

class EmployeeBuilder:
    """
    Esta classe nos ajuda a construir um objeto Employee passo a passo.
    """
    def __init__(self, name, age, email):
        # Atributos essenciais são passados no início
        self.name = name
        self.age = age
        self.email = email
        # Outros atributos começam com valores padrão
        self.department = "Not Assigned"
        self.work_position = "Not Assigned"
        self.salary_per_hour = 0
        self.hire_date = "Not Defined"
        self.emp_type = 1 # 1 para Employee padrão

    def set_type(self, emp_type):
        self.emp_type = emp_type
        return self # Retornar 'self' permite encadear chamadas

    def set_details(self, department, work_position, hire_date):
        self.department = department
        self.work_position = work_position
        self.hire_date = hire_date
        return self

    def set_salary(self, salary_per_hour):
        self.salary_per_hour = salary_per_hour
        return self

    def build(self):
        """
        Usa todos os dados fornecidos para construir o objeto final.
        """
        if self.emp_type == 2:
            return Manager(self.name, self.age, self.email, self.department, self.salary_per_hour, self.hire_date)
        elif self.emp_type == 3:
            return Intern(self.name, self.age, self.email, self.department, self.salary_per_hour, self.hire_date)
        else:
            return Employee(self.name, self.age, self.email, self.department, self.work_position, self.salary_per_hour, self.hire_date)