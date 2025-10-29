# facade.py

from hr_system import HRSystem
from factories import EmployeeFactory
from models import Employee, Manager
from services import (
    PaymentContext, HourlyPaymentStrategy, MonthlyPaymentStrategy,
    PaymentStrategy, ManagerBonusDecorator, TaxDeductionDecorator
)

# PADRÃO ESTRUTURAL 3: FACADE
# Objetivo: Fornecer uma interface simplificada para um conjunto complexo
# de subsistemas, facilitando o uso do sistema.

class HRFacade:
    """
    A Fachada que simplifica a interação com os subsistemas de RH
    (Singleton, Factory, Strategy, Decorator).
    """
    def __init__(self):
        # A Fachada obtém acesso ao Singleton para gerenciar o estado
        self._hr_system = HRSystem.get_instance()

    def get_employee_list(self) -> list[Employee]:
        """ Retorna a lista de funcionários do subsistema. """
        return self._hr_system.employees_list

    def hire_employee(self, emp_type, name, age, email, dept, pos, salary, hire_date) -> Employee:
        """
        Simplifica o processo de contratação.
        Internamente, usa a Factory e o Singleton.
        """
        print(f"\n[Facade] Contratando {name}...")
        
        # 1. Usa a Factory para criar o objeto complexo
        new_employee = EmployeeFactory.create_employee(
            emp_type, name, age, email, dept, pos, salary, hire_date
        )
        
        # 2. Usa o Singleton para adicionar ao sistema
        self._hr_system.add_employee(new_employee)
        
        print(f"[Facade] {name} contratado e adicionado ao sistema.")
        return new_employee

    def remove_employee(self, index: int):
        """ Simplifica a remoção de um funcionário. """
        self._hr_system.remove_employee(index)

    def calculate_payment(self, employee_index: int) -> float:
        """
        Simplifica todo o processo de cálculo de pagamento.
        Internamente, usa o Singleton, o Strategy e o Decorator.
        """
        if not (0 <= employee_index < len(self._hr_system.employees_list)):
            raise IndexError("Índice de funcionário inválido.")
            
        employee = self._hr_system.employees_list[employee_index]
        attendance = self._hr_system.attendance_list[employee_index]
        
        print(f"\n[Facade] Calculando pagamento para: {employee.name}...")

        # 1. Começa com a estratégia base (Padrão Strategy)
        payment_strategy: PaymentStrategy = HourlyPaymentStrategy()
        
        # 2. "Decora" a estratégia base (Padrão Decorator)
        if isinstance(employee, Manager):
            payment_strategy = ManagerBonusDecorator(payment_strategy)
        
        # 3. "Decora" novamente com o imposto
        payment_strategy = TaxDeductionDecorator(payment_strategy)

        # 4. O Contexto usa a estratégia final
        payment_context = PaymentContext(payment_strategy)
        money = payment_context.calculate_payment(attendance, employee.salary_per_hour)
        
        print(f"----------------------------------------")
        print(f"[Facade] Salário líquido: R$ {money:.2f}")
        return money

    def generate_attendance_report(self, employee_index: int):
        """ Simplifica a geração do relatório de frequência. """
        if 0 <= employee_index < len(self._hr_system.attendance_list):
            report = self._hr_system.attendance_list[employee_index]
            report.generate_report()
        else:
            raise IndexError("Índice de funcionário inválido.")

    def generate_compliance_report(self, employee_index: int):
        """ Simplifica a geração do relatório de compliance. """
        if 0 <= employee_index < len(self._hr_system.compliance_list):
            report = self._hr_system.compliance_list[employee_index]
            report.generate_report()
        else:
            raise IndexError("Índice de funcionário inválido.")