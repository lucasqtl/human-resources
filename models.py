# models.py
from abc import ABC, abstractmethod

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

# CORREÇÃO: A classe base 'Person' foi movida para ANTES da classe 'Employee'.
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
        if isinstance(value, str) and len(value) > 0:
            self._name = value
        else:
            raise ValueError("Name must be a non-empty string")
    
    @property
    def age(self):
        return self._age
    
    @age.setter
    def age(self, value):
        if isinstance(value, int) and value > 0:
            self._age = value
        else:
            raise ValueError("Age must be a positive number")
    
    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, value):
        if "@" in value:
            self._email = value
        else:
            raise ValueError("Email must contain @")
    
    @abstractmethod
    def get_role(self):
        pass
    
    @abstractmethod
    def display_info(self):
        pass

# Agora, Employee pode herdar de Person sem problemas.
class Employee(Person, Subject):
    number_of_employees = 0
    
    def __init__(self, name, age, email, department, work_position, salary_per_hour, hire_date):
        Person.__init__(self, name, age, email)
        Subject.__init__(self) # Inicializa a lógica do Subject
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
        if isinstance(value, str) and len(value) > 0:
            self._department = value
        else:
            raise ValueError("Department must be a non-empty string")
    
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
        if isinstance(value, (int, float)) and value > 0:
            self._salary_per_hour = value
            self.notify() # Notifica observers sempre que o salário muda.
        else:
            raise ValueError("Salary must be a positive number")
    
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

    def add_leave_request(self, start_date, end_date, reason):
        leave = {"f_Date": start_date, "s_Date": end_date, "Description": reason}
        self._requests.append(leave)
    
    def remove_leave_request(self, index):
        if 0 <= index < len(self._requests):
            self._requests.pop(index)
        else:
            print("Invalid index")
    
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
        if 0 <= index < len(self._training):
            self._training.pop(index)
        else:
            print("Invalid Index")
    
    def show_training(self):
        print(f"Training sessions for {self._name}")
        if not self._training:
            print("No sessions scheduled.")
        else:
            for i, session in enumerate(self._training, 1):
                print(f"{i}) {session['Date']} at {session['Time']} - {session['Description']}")
    
    def add_performance_evaluation(self, level):
        performance_levels = {1: "Good", 2: "Average", 3: "Bad"}
        if level in performance_levels:
            self._performance.append(level)
        else:
            print("Invalid input")
    
    def remove_performance_evaluation(self, index):
        if 0 <= index < len(self._performance):
            self._performance.pop(index)
        else:
            print("Invalid index")
    
    def show_performance(self):
        performance_levels = {1: "Good", 2: "Average", 3: "Bad"}
        print(f"\nPerformance of {self._name}:")
        if self._performance:
            for i, level in enumerate(self._performance, 1):
                print(f"{i}) {performance_levels[level]}")
        else:
            print("No evaluations found.")

    def add_benefit(self, benefit):
        if benefit not in self._benefits:
            self._benefits.append(benefit)
        else:
            print("Benefit already added.")
    
    def remove_benefit(self, benefit):
        if benefit in self._benefits:
            self._benefits.remove(benefit)
        else:
            print("Benefit not found.")


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
        print(f"Mentor: {self._mentor.name if self._mentor else 'Not assigned'}")