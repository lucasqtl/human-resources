# models.py
from abc import ABC, abstractmethod
from exceptions import (
    InvalidNameException, InvalidAgeException, InvalidEmailException,
    InvalidDepartmentException, InvalidSalaryException, InvalidIndexException,
    InvalidPerformanceLevelException, BenefitAlreadyExistsException,
    BenefitNotFoundException
)

# Padrão Observer - Classes Base
class Observer(ABC):
    @abstractmethod
    def update(self, subject):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer: Observer):
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self):
        for observer in self._observers:
            observer.update(self)

# PADRÃO ESTRUTURAL 1: COMPOSITE (Interface)
# Objetivo: Definir uma interface comum para objetos 'folha' (Employee)
# e objetos 'compostos' (Department), permitindo que sejam tratados uniformemente.
class OrganizationalComponent(ABC):
    
    @abstractmethod
    def display_hierarchy(self, indent_level: int = 0):
        """ Exibe a hierarquia organizacional. """
        pass
    
    @abstractmethod
    def get_role(self) -> str:
        """ Retorna a função/cargo do componente. """
        pass


class Person(ABC):
    """
    Classe Abstrata que serve como um modelo base para qualquer 'pessoa' no sistema.
    """
    def __init__(self, name, age, email):
        self._name = name
        self._age = age
        self._email = email

    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        try:
            if not isinstance(value, str):
                raise TypeError(f"Nome deve ser uma string, recebido: {type(value).__name__}")
            if len(value.strip()) == 0:
                raise InvalidNameException("Nome não pode ser vazio ou conter apenas espaços em branco")
            if len(value) > 100:
                raise InvalidNameException("Nome não pode ter mais de 100 caracteres")
            self._name = value.strip()
        except (TypeError, InvalidNameException) as e:
            raise InvalidNameException(f"Erro ao definir nome: {str(e)}")
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        try:
            if not isinstance(value, int):
                if isinstance(value, float):
                    raise TypeError("Idade deve ser um número inteiro, não um número decimal")
                raise TypeError(f"Idade deve ser um número inteiro, recebido: {type(value).__name__}")
            if value <= 0:
                raise InvalidAgeException(f"Idade deve ser um número positivo, recebido: {value}")
            if value < 16:
                raise InvalidAgeException(f"Idade mínima permitida é 16 anos, recebido: {value}")
            if value > 100:
                raise InvalidAgeException(f"Idade máxima permitida é 100 anos, recebido: {value}")
            self._age = value
        except (TypeError, InvalidAgeException) as e:
            raise InvalidAgeException(f"Erro ao definir idade: {str(e)}")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        try:
            if not isinstance(value, str):
                raise TypeError(f"Email deve ser uma string, recebido: {type(value).__name__}")
            if len(value.strip()) == 0:
                raise InvalidEmailException("Email não pode ser vazio")
            if "@" not in value:
                raise InvalidEmailException("Email deve conter o símbolo '@'")
            if value.count("@") > 1:
                raise InvalidEmailException("Email deve conter apenas um símbolo '@'")
            if "." not in value.split("@")[1] if "@" in value else "":
                raise InvalidEmailException("Email deve ter um domínio válido (ex: exemplo@dominio.com)")
            if len(value) > 255:
                raise InvalidEmailException("Email não pode ter mais de 255 caracteres")
            self._email = value.strip().lower()
        except (TypeError, InvalidEmailException) as e:
            raise InvalidEmailException(f"Erro ao definir email: {str(e)}")
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def display_info(self):
        pass

class Employee(Person, Subject, OrganizationalComponent):
    number_of_employees = 0
    
    def __init__(self, name, age, email, department, work_position, salary_per_hour, hire_date):
        Person.__init__(self, name, age, email)
        Subject.__init__(self) 
        self._department = department
        self._work_position = work_position
        self._salary_per_hour = salary_per_hour
        self._hire_date = hire_date
        self._benefits = []
        self._performance = []
        self._training = []
        self._requests = []
        Employee.number_of_employees += 1
    
    @property
    def department(self):
        return self._department
    
    @department.setter
    def department(self, value):
        try:
            if not isinstance(value, str):
                raise TypeError(f"Departamento deve ser uma string, recebido: {type(value).__name__}")
            if len(value.strip()) == 0:
                raise InvalidDepartmentException("Departamento não pode ser vazio ou conter apenas espaços")
            if len(value) > 100:
                raise InvalidDepartmentException("Departamento não pode ter mais de 100 caracteres")
            self._department = value.strip()
        except (TypeError, InvalidDepartmentException) as e:
            raise InvalidDepartmentException(f"Erro ao definir departamento: {str(e)}")
    
    @property
    def work_position(self):
        return self._work_position
    
    @work_position.setter
    def work_position(self, value):
        self._work_position = value
    
    @property
    def salary_per_hour(self):
        return self._salary_per_hour
    
    @salary_per_hour.setter
    def salary_per_hour(self, value):
        try:
            if not isinstance(value, (int, float)):
                raise TypeError(f"Salário deve ser um número, recebido: {type(value).__name__}")
            if value <= 0:
                raise InvalidSalaryException(f"Salário deve ser um número positivo, recebido: {value}")
            if value < 1.0:
                raise InvalidSalaryException(f"Salário por hora deve ser no mínimo R$ 1,00, recebido: R$ {value:.2f}")
            if value > 10000.0:
                raise InvalidSalaryException(f"Salário por hora não pode exceder R$ 10.000,00, recebido: R$ {value:.2f}")
            self._salary_per_hour = float(value)
            self.notify() 
        except (TypeError, InvalidSalaryException) as e:
            raise InvalidSalaryException(f"Erro ao definir salário: {str(e)}")
    
    @property
    def hire_date(self):
        return self._hire_date
    
    @hire_date.setter
    def hire_date(self, value):
        self._hire_date = value
    
    def get_role(self):
        return f"Employee - {self._work_position}"
    
    def display_info(self):
        print(f"Name: {self._name}")
        print(f"Age: {self._age}")
        print(f"Email: {self._email}")
        print(f"Department: {self._department}")
        print(f"Position: {self._work_position}")
        print(f"Salary per hour: R$ {self._salary_per_hour:.2f}")
        print(f"Hire Date: {self._hire_date}")
        print(f"Benefits: {', '.join(self._benefits) if self._benefits else 'None'}")
    
    def __str__(self):
        return self._name

    # Implementação do Padrão Composite (Leaf)
    def display_hierarchy(self, indent_level: int = 0):
        indent = "  " * indent_level
        print(f"{indent}- {self.name} ({self.get_role()})")

    def add_leave_request(self, start_date, end_date, reason):
        leave = {"f_Date": start_date, "s_Date": end_date, "Description": reason}
        self._requests.append(leave)
    
    def remove_leave_request(self, index):
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if index >= len(self._requests):
                raise InvalidIndexException(f"Índice {index} está fora do range. Total de solicitações: {len(self._requests)}")
            if len(self._requests) == 0:
                raise InvalidIndexException("Não há solicitações de afastamento para remover")
            self._requests.pop(index)
        except (TypeError, InvalidIndexException) as e:
            raise InvalidIndexException(f"Erro ao remover solicitação de afastamento: {str(e)}")
    
    def show_leave_requests(self):
        print(f"Leave requests for {self._name}")
        if not self._requests:
            print("No leave requests.")
        else:
            for i, leave in enumerate(self._requests, 1):
                print(f"{i}) {leave['f_Date']} to {leave['s_Date']} - {leave['Description']}")

    def add_training(self, date_str, time_str, description):
        session = {"Date": date_str, "Time": time_str, "Description": description}
        self._training.append(session)
    
    def remove_training(self, index):
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if index >= len(self._training):
                raise InvalidIndexException(f"Índice {index} está fora do range. Total de treinamentos: {len(self._training)}")
            if len(self._training) == 0:
                raise InvalidIndexException("Não há treinamentos para remover")
            self._training.pop(index)
        except (TypeError, InvalidIndexException) as e:
            raise InvalidIndexException(f"Erro ao remover treinamento: {str(e)}")
    
    def show_training(self):
        print(f"Training sessions for {self._name}")
        if not self._training:
            print("No sessions scheduled.")
        else:
            for i, session in enumerate(self._training, 1):
                print(f"{i}) {session['Date']} at {session['Time']} - {session['Description']}")
    
    def add_performance_evaluation(self, level):
        try:
            performance_levels = {1: "Good", 2: "Average", 3: "Bad"}
            if not isinstance(level, int):
                raise TypeError(f"Nível de performance deve ser um número inteiro, recebido: {type(level).__name__}")
            if level not in performance_levels:
                raise InvalidPerformanceLevelException(
                    f"Nível de performance deve ser 1 (Good), 2 (Average) ou 3 (Bad), recebido: {level}"
                )
            self._performance.append(level)
        except (TypeError, InvalidPerformanceLevelException) as e:
            raise InvalidPerformanceLevelException(f"Erro ao adicionar avaliação de performance: {str(e)}")
    
    def remove_performance_evaluation(self, index):
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if index >= len(self._performance):
                raise InvalidIndexException(f"Índice {index} está fora do range. Total de avaliações: {len(self._performance)}")
            if len(self._performance) == 0:
                raise InvalidIndexException("Não há avaliações de performance para remover")
            self._performance.pop(index)
        except (TypeError, InvalidIndexException) as e:
            raise InvalidIndexException(f"Erro ao remover avaliação de performance: {str(e)}")
    
    def show_performance(self):
        performance_levels = {1: "Good", 2: "Average", 3: "Bad"}
        print(f"\nPerformance of {self._name}:")
        if self._performance:
            for i, level in enumerate(self._performance, 1):
                print(f"{i}) {performance_levels[level]}")
        else:
            print("No evaluations found.")

    def add_benefit(self, benefit):
        try:
            if not isinstance(benefit, str):
                raise TypeError(f"Benefício deve ser uma string, recebido: {type(benefit).__name__}")
            if len(benefit.strip()) == 0:
                raise ValueError("Benefício não pode ser vazio ou conter apenas espaços")
            if benefit in self._benefits:
                raise BenefitAlreadyExistsException(f"O benefício '{benefit}' já foi adicionado para este funcionário")
            self._benefits.append(benefit.strip())
        except (TypeError, ValueError, BenefitAlreadyExistsException) as e:
            raise BenefitAlreadyExistsException(f"Erro ao adicionar benefício: {str(e)}")
    
    def remove_benefit(self, benefit):
        try:
            if not isinstance(benefit, str):
                raise TypeError(f"Benefício deve ser uma string, recebido: {type(benefit).__name__}")
            if benefit not in self._benefits:
                raise BenefitNotFoundException(f"O benefício '{benefit}' não foi encontrado para este funcionário")
            if len(self._benefits) == 0:
                raise BenefitNotFoundException("Não há benefícios para remover")
            self._benefits.remove(benefit)
        except (TypeError, BenefitNotFoundException) as e:
            raise BenefitNotFoundException(f"Erro ao remover benefício: {str(e)}")


class Manager(Employee):
    """
    Representa um Gerente, que é um tipo especial de Funcionário.
    """
    def __init__(self, name, age, email, department, salary_per_hour, hire_date, team_size=0):
        super().__init__(name, age, email, department, "Manager", salary_per_hour, hire_date)
        self._team_size = team_size
        self._managed_employees = []
    
    def get_role(self):
        return f"Manager - {self._department} Department"
    
    def display_info(self):
        super().display_info()
        print(f"Team Size: {self._team_size}")
        print(f"Managed Employees: {len(self._managed_employees)}")


class Intern(Employee):
    """
    Representa um Estagiário, outro tipo especial de Funcionário.
    """
    def __init__(self, name, age, email, department, salary_per_hour, hire_date, mentor=None):
        super().__init__(name, age, email, department, "Intern", salary_per_hour, hire_date)
        self._mentor = mentor
    
    def get_role(self):
        return f"Intern - {self._department} Department"
    
    def display_info(self):
        super().display_info()
        try:
            mentor_name = self._mentor.name if self._mentor else 'Not assigned'
            print(f"Mentor: {mentor_name}")
        except AttributeError:
            print(f"Mentor: Not assigned (erro ao acessar informações do mentor)")


# PADRÃO ESTRUTURAL 1: COMPOSITE (Classe Composite)
# Esta classe pode conter outros componentes (Leaves ou outros Composites)
class Department(OrganizationalComponent):
    """
    Representa um Departamento, que é um 'Composite'.
    Ele pode conter 'Leaves' (Employees) ou outros 'Composites' (Sub-departamentos).
    """
    def __init__(self, name: str):
        self._name = name
        self._children: list[OrganizationalComponent] = []

    def add_component(self, component: OrganizationalComponent):
        self._children.append(component)

    def remove_component(self, component: OrganizationalComponent):
        try:
            if component is None:
                raise ValueError("Componente não pode ser None")
            if component not in self._children:
                raise ValueError(f"Componente '{component.get_role() if hasattr(component, 'get_role') else str(component)}' não encontrado no departamento")
            self._children.remove(component)
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Erro ao remover componente: {str(e)}")

    def get_role(self) -> str:
        return f"Department - {self._name}"

    def display_hierarchy(self, indent_level: int = 0):
        indent = "  " * indent_level
        print(f"{indent}+ {self._name} (Departamento)")
        
        for child in self._children:
            child.display_hierarchy(indent_level + 1)