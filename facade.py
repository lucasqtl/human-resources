# facade.py

from hr_system import HRSystem
from factories import EmployeeFactory
from models import Employee, Manager
from services import (
    PaymentContext, HourlyPaymentStrategy, MonthlyPaymentStrategy,
    PaymentStrategy, ManagerBonusDecorator, TaxDeductionDecorator
)
from exceptions import (
    InvalidEmployeeIndexException, InvalidEmployeeDataException,
    InvalidEmployeeTypeException, HRSystemException
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
        self._hr_system = HRSystem.get_instance()

    def get_employee_list(self) -> list[Employee]:
        """ Retorna a lista de funcionários do subsistema. """
        return self._hr_system.employees_list

    def hire_employee(self, emp_type, name, age, email, dept, pos, salary, hire_date) -> Employee:
        """
        Simplifica o processo de contratação.
        Internamente, usa a Factory e o Singleton.
        """
        try:
            if emp_type not in [1, 2, 3]:
                raise InvalidEmployeeTypeException(f"Tipo de funcionário deve ser 1, 2 ou 3, recebido: {emp_type}")
            
            if not name or not isinstance(name, str) or len(name.strip()) == 0:
                raise InvalidEmployeeDataException("Nome do funcionário não pode ser vazio")
            
            if not isinstance(age, int) or age <= 0:
                raise InvalidEmployeeDataException(f"Idade deve ser um número inteiro positivo, recebido: {age}")
            
            if not email or not isinstance(email, str) or len(email.strip()) == 0:
                raise InvalidEmployeeDataException("Email do funcionário não pode ser vazio")
            
            if not dept or not isinstance(dept, str) or len(dept.strip()) == 0:
                raise InvalidEmployeeDataException("Departamento não pode ser vazio")
            
            if not isinstance(salary, (int, float)) or salary <= 0:
                raise InvalidEmployeeDataException(f"Salário deve ser um número positivo, recebido: {salary}")
            
            print(f"\n[Facade] Contratando {name}...")
            
            new_employee = EmployeeFactory.create_employee(
                emp_type, name, age, email, dept, pos, salary, hire_date
            )
            
            self._hr_system.add_employee(new_employee)
            
            print(f"[Facade] {name} contratado e adicionado ao sistema.")
            return new_employee
        except (InvalidEmployeeTypeException, InvalidEmployeeDataException) as e:
            raise
        except Exception as e:
            raise HRSystemException(f"Erro ao contratar funcionário: {str(e)}")

    def remove_employee(self, index: int):
        """ Simplifica a remoção de um funcionário. """
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidEmployeeIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if index >= len(self._hr_system.employees_list):
                raise InvalidEmployeeIndexException(
                    f"Índice {index} está fora do range. Total de funcionários: {len(self._hr_system.employees_list)}"
                )
            self._hr_system.remove_employee(index)
        except (TypeError, InvalidEmployeeIndexException) as e:
            raise InvalidEmployeeIndexException(f"Erro ao remover funcionário: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro no sistema ao remover funcionário: {str(e)}")

    def calculate_payment(self, employee_index: int) -> float:
        """
        Simplifica todo o processo de cálculo de pagamento.
        Internamente, usa o Singleton, o Strategy e o Decorator.
        """
        try:
            if not isinstance(employee_index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(employee_index).__name__}")
            if employee_index < 0:
                raise InvalidEmployeeIndexException(f"Índice não pode ser negativo, recebido: {employee_index}")
            if employee_index >= len(self._hr_system.employees_list):
                raise InvalidEmployeeIndexException(
                    f"Índice {employee_index} está fora do range. Total de funcionários: {len(self._hr_system.employees_list)}"
                )
            if employee_index >= len(self._hr_system.attendance_list):
                raise InvalidEmployeeIndexException(
                    f"Lista de frequência dessincronizada. Índice {employee_index} não existe na lista de frequência"
                )
            
            employee = self._hr_system.employees_list[employee_index]
            attendance = self._hr_system.attendance_list[employee_index]
            
            print(f"\n[Facade] Calculando pagamento para: {employee.name}...")

            payment_strategy: PaymentStrategy = HourlyPaymentStrategy()
            
            if isinstance(employee, Manager):
                payment_strategy = ManagerBonusDecorator(payment_strategy)
            
            payment_strategy = TaxDeductionDecorator(payment_strategy)

            payment_context = PaymentContext(payment_strategy)
            money = payment_context.calculate_payment(attendance, employee.salary_per_hour)
            
            print(f"----------------------------------------")
            print(f"[Facade] Salário líquido: R$ {money:.2f}")
            return money
        except (TypeError, InvalidEmployeeIndexException) as e:
            raise InvalidEmployeeIndexException(f"Erro ao calcular pagamento: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro no sistema ao calcular pagamento: {str(e)}")

    def generate_attendance_report(self, employee_index: int):
        """ Simplifica a geração do relatório de frequência. """
        try:
            if not isinstance(employee_index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(employee_index).__name__}")
            if employee_index < 0:
                raise InvalidEmployeeIndexException(f"Índice não pode ser negativo, recebido: {employee_index}")
            if employee_index >= len(self._hr_system.attendance_list):
                raise InvalidEmployeeIndexException(
                    f"Índice {employee_index} está fora do range. Total de registros de frequência: {len(self._hr_system.attendance_list)}"
                )
            report = self._hr_system.attendance_list[employee_index]
            report.generate_report()
        except (TypeError, InvalidEmployeeIndexException) as e:
            raise InvalidEmployeeIndexException(f"Erro ao gerar relatório de frequência: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro no sistema ao gerar relatório de frequência: {str(e)}")

    def generate_compliance_report(self, employee_index: int):
        """ Simplifica a geração do relatório de compliance. """
        try:
            if not isinstance(employee_index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(employee_index).__name__}")
            if employee_index < 0:
                raise InvalidEmployeeIndexException(f"Índice não pode ser negativo, recebido: {employee_index}")
            if employee_index >= len(self._hr_system.compliance_list):
                raise InvalidEmployeeIndexException(
                    f"Índice {employee_index} está fora do range. Total de registros de compliance: {len(self._hr_system.compliance_list)}"
                )
            report = self._hr_system.compliance_list[employee_index]
            report.generate_report()
        except (TypeError, InvalidEmployeeIndexException) as e:
            raise InvalidEmployeeIndexException(f"Erro ao gerar relatório de compliance: {str(e)}")
        except Exception as e:
            raise HRSystemException(f"Erro no sistema ao gerar relatório de compliance: {str(e)}")