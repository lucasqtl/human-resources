# services.py
from datetime import datetime
from abc import ABC, abstractmethod
from models import Employee
from exceptions import (
    ClockInWithoutClockOutException, ClockOutWithoutClockInException,
    NoAttendanceRecordsException, InvalidPaymentCalculationException,
    NegativePaymentException, InvalidIndexException, InvalidDateException,
    InvalidTimeException, AttendanceException
)

# PADRÃO COMPORTAMENTAL 3: TEMPLATE METHOD
# Objetivo: Definir o esqueleto de um algoritmo, adiando a implementação de
# passos específicos para as subclasses.
class Report(ABC):
    def __init__(self, employee: Employee):
        self._employee = employee
    
    def generate_report(self):
        """ Gera um relatório completo seguindo uma estrutura pré-definida. """
        header = self._generate_header()
        body = self._generate_body()
        footer = self._generate_footer()
        
        report = f"{header}\n{'-'*40}\n{body}\n{'-'*40}\n{footer}"
        print(report)

    @abstractmethod
    def _generate_header(self) -> str:
        """ Gera o cabeçalho específico do relatório. """
        pass

    @abstractmethod
    def _generate_body(self) -> str:
        """ Gera o corpo principal do relatório. """
        pass

    def _generate_footer(self) -> str:
        """ Gera um rodapé padrão para todos os relatórios. """
        return f"Relatório gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


class Attendance(Report):
    def __init__(self, employee: Employee):
        super().__init__(employee)
        self._record = []
    
    def clock_in(self):
        try:
            now = datetime.now()
            # Verifica se há um registro anterior sem clock out
            if self._record and self._record[-1]["out"] is None:
                raise ClockInWithoutClockOutException(
                    f"Não é possível fazer clock in: há um registro anterior sem clock out. "
                    f"Último clock in: {self._record[-1]['in'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
            self._record.append({"in": now, "out": None})
            print(f"{self._employee.name} clocked in at {now.strftime('%H:%M:%S')}")
        except ClockInWithoutClockOutException:
            raise
        except Exception as e:
            raise AttendanceException(f"Erro ao registrar entrada: {str(e)}")
    
    def clock_out(self):
        try:
            now = datetime.now()
            if not self._record:
                raise ClockOutWithoutClockInException(
                    f"Não é possível fazer clock out: não há registro de clock in anterior para {self._employee.name}"
                )
            if self._record[-1]["out"] is not None:
                raise ClockOutWithoutClockInException(
                    f"Não é possível fazer clock out: último registro já possui clock out. "
                    f"Último clock out: {self._record[-1]['out'].strftime('%Y-%m-%d %H:%M:%S')}"
                )
            # Verifica se o clock out não é anterior ao clock in
            if now < self._record[-1]["in"]:
                raise InvalidTimeException(
                    f"Clock out não pode ser anterior ao clock in. "
                    f"Clock in: {self._record[-1]['in'].strftime('%Y-%m-%d %H:%M:%S')}, "
                    f"Clock out tentado: {now.strftime('%Y-%m-%d %H:%M:%S')}"
                )
            self._record[-1]["out"] = now
            print(f"{self._employee.name} clocked out at {now.strftime('%H:%M:%S')}")
        except (ClockOutWithoutClockInException, InvalidTimeException) as e:
            raise
        except Exception as e:
            raise AttendanceException(f"Erro ao registrar saída: {str(e)}")
    
    def show_records(self):
        try:
            if not self._record:
                raise NoAttendanceRecordsException(f"Não há registros de frequência para {self._employee.name}")
            print(f"\nRecords of {self._employee.name}: ")
            for i, record in enumerate(self._record, 1):
                try:
                    in_time = record['in'].strftime('%Y-%m-%d %H:%M:%S')
                    out_time = record['out'].strftime('%Y-%m-%d %H:%M:%S') if record['out'] else "Still working"
                    print(f"{i}) IN: {in_time} | OUT: {out_time}")
                except KeyError as e:
                    raise AttendanceException(f"Erro ao acessar dados do registro {i}: campo '{e}' não encontrado")
                except AttributeError as e:
                    raise AttendanceException(f"Erro ao formatar data do registro {i}: {str(e)}")
        except (NoAttendanceRecordsException, AttendanceException) as e:
            raise
        except Exception as e:
            raise AttendanceException(f"Erro ao exibir registros: {str(e)}")

    def worked_hours_per_day(self):
        try:
            if not self._record:
                raise NoAttendanceRecordsException(f"Não há registros de frequência para calcular horas trabalhadas de {self._employee.name}")
            
            print(f"\nWorked hours for {self._employee.name}:")
            total_seconds = 0
            valid_records = 0
            
            for i, record in enumerate(self._record, 1):
                try:
                    if "in" not in record:
                        raise AttendanceException(f"Registro {i} não possui campo 'in'")
                    if record["out"] is not None:
                        if "out" not in record:
                            raise AttendanceException(f"Registro {i} não possui campo 'out'")
                        worked = record["out"] - record["in"]
                        if worked.total_seconds() < 0:
                            raise InvalidTimeException(
                                f"Registro {i}: tempo trabalhado negativo. "
                                f"Clock in: {record['in']}, Clock out: {record['out']}"
                            )
                        total_seconds += worked.total_seconds()
                        valid_records += 1
                        print(f"- {record['in'].strftime('%Y-%m-%d')}: {worked}")
                except KeyError as e:
                    raise AttendanceException(f"Erro ao processar registro {i}: campo '{e}' não encontrado")
                except (AttributeError, TypeError) as e:
                    raise AttendanceException(f"Erro ao processar registro {i}: {str(e)}")
            
            if valid_records == 0:
                raise NoAttendanceRecordsException(
                    f"Não há registros completos (com clock out) para {self._employee.name}"
                )
            
            total_hours = total_seconds // 3600
            total_minutes = (total_seconds % 3600) // 60
            print(f"\nTotal worked time: {int(total_hours)}h {int(total_minutes)}min\n")
        except (NoAttendanceRecordsException, AttendanceException, InvalidTimeException) as e:
            raise
        except Exception as e:
            raise AttendanceException(f"Erro ao calcular horas trabalhadas: {str(e)}")
    
    def _generate_header(self) -> str:
        return f"Relatório de Frequência para {self._employee.name}"

    def _generate_body(self) -> str:
        if not self._record:
            return "Nenhum registro de frequência encontrado."
        
        body_str = "Registros:\n"
        for record in self._record:
            in_time = record['in'].strftime('%Y-%m-%d %H:%M:%S')
            out_time = record['out'].strftime('%Y-%m-%d %H:%M:%S') if record['out'] else "Ainda trabalhando"
            body_str += f" - Entrada: {in_time} | Saída: {out_time}\n"
        return body_str


# PADRÃO COMPORTAMENTAL 1: STRATEGY
# Objetivo: Permitir que o algoritmo de cálculo de pagamento seja selecionado em tempo de execução.
class PaymentStrategy(ABC):
    """ A Interface da Estratégia declara operações comuns a todos os algoritmos suportados. """
    @abstractmethod
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        pass

class HourlyPaymentStrategy(PaymentStrategy):
    """ Estratégia Concreta: Calcula o pagamento com base nas horas trabalhadas. """
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        try:
            if not attendance._record:
                raise NoAttendanceRecordsException(
                    f"Não há registros de frequência para calcular pagamento de {attendance._employee.name}"
                )
            if salary_per_hour <= 0:
                raise InvalidPaymentCalculationException(f"Salário por hora deve ser positivo, recebido: {salary_per_hour}")
            
            total_seconds = 0
            valid_records = 0
            
            for i, record in enumerate(attendance._record, 1):
                try:
                    if "in" not in record or "out" not in record:
                        continue
                    if record["in"] and record["out"]:
                        worked = record["out"] - record["in"]
                        worked_seconds = worked.total_seconds()
                        if worked_seconds < 0:
                            raise InvalidPaymentCalculationException(
                                f"Registro {i} possui tempo trabalhado negativo: {worked}"
                            )
                        total_seconds += worked_seconds
                        valid_records += 1
                except (KeyError, AttributeError, TypeError) as e:
                    raise InvalidPaymentCalculationException(f"Erro ao processar registro {i}: {str(e)}")
            
            if valid_records == 0:
                raise NoAttendanceRecordsException(
                    f"Não há registros completos (com clock in e clock out) para calcular pagamento"
                )
            
            total_hours = total_seconds / 3600
            if total_hours == 0:
                raise InvalidPaymentCalculationException("Total de horas trabalhadas é zero")
            
            payment = total_hours * salary_per_hour
            if payment < 0:
                raise NegativePaymentException(f"Pagamento calculado é negativo: R$ {payment:.2f}")
            
            print(f"  -> Salário Base (Horista): R$ {payment:.2f}")
            return payment
        except (NoAttendanceRecordsException, InvalidPaymentCalculationException, NegativePaymentException) as e:
            raise
        except Exception as e:
            raise InvalidPaymentCalculationException(f"Erro ao calcular pagamento horista: {str(e)}")

class MonthlyPaymentStrategy(PaymentStrategy):
    """ Estratégia Concreta: Calcula um pagamento fixo mensal (ex: 160 horas de trabalho). """
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        try:
            FIXED_HOURS_PER_MONTH = 160
            if salary_per_hour <= 0:
                raise InvalidPaymentCalculationException(f"Salário por hora deve ser positivo, recebido: {salary_per_hour}")
            if salary_per_hour > 10000:
                raise InvalidPaymentCalculationException(f"Salário por hora excede o limite máximo: R$ {salary_per_hour:.2f}")
            
            payment = FIXED_HOURS_PER_MONTH * salary_per_hour
            if payment < 0:
                raise NegativePaymentException(f"Pagamento calculado é negativo: R$ {payment:.2f}")
            
            print(f"  -> Salário Base (Mensalista): R$ {payment:.2f}")
            return payment
        except (InvalidPaymentCalculationException, NegativePaymentException) as e:
            raise
        except Exception as e:
            raise InvalidPaymentCalculationException(f"Erro ao calcular pagamento mensalista: {str(e)}")

class PaymentContext:
    """
    O Contexto (antes chamado de Payment) mantém uma referência a uma das estratégias.
    Ele não conhece os detalhes da estratégia, apenas a utiliza.
    """
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def calculate_payment(self, attendance: Attendance, salary_per_hour: float):
        """ O Contexto delega o trabalho de cálculo para o objeto da Estratégia. """
        return self._strategy.calculate(attendance, salary_per_hour)


# PADRÃO ESTRUTURAL 2: DECORATOR
# Objetivo: Adicionar responsabilidades a um objeto dinamicamente,
# sem alterar a classe do objeto original.

class BasePaymentDecorator(PaymentStrategy):
    """
    O Decorator base segue a mesma interface do componente que ele
    decora. Ele armazena uma referência ao objeto "embrulhado".
    """
    _wrapped_strategy: PaymentStrategy = None

    def __init__(self, strategy: PaymentStrategy):
        self._wrapped_strategy = strategy

    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        return self._wrapped_strategy.calculate(attendance, salary_per_hour)

class ManagerBonusDecorator(BasePaymentDecorator):
    """
    Este Decorator Concreto adiciona um bônus de 20% para gerentes.
    """
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        try:
            base_pay = self._wrapped_strategy.calculate(attendance, salary_per_hour)
            
            if base_pay < 0:
                raise NegativePaymentException(f"Pagamento base é negativo: R$ {base_pay:.2f}")
            
            bonus = base_pay * 0.20
            if bonus < 0:
                raise InvalidPaymentCalculationException(f"Bônus calculado é negativo: R$ {bonus:.2f}")
            
            final_payment = base_pay + bonus
            if final_payment < 0:
                raise NegativePaymentException(f"Pagamento final é negativo: R$ {final_payment:.2f}")
            
            print(f"  -> Bônus (Manager 20%): +R$ {bonus:.2f}")
            return final_payment
        except (NegativePaymentException, InvalidPaymentCalculationException) as e:
            raise
        except Exception as e:
            raise InvalidPaymentCalculationException(f"Erro ao calcular bônus de gerente: {str(e)}")

class TaxDeductionDecorator(BasePaymentDecorator):
    """
    Este Decorator Concreto aplica um desconto de 15% de imposto.
    """
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        try:
            gross_pay = self._wrapped_strategy.calculate(attendance, salary_per_hour)
            
            if gross_pay < 0:
                raise NegativePaymentException(f"Pagamento bruto é negativo: R$ {gross_pay:.2f}")
            
            tax = gross_pay * 0.15
            if tax < 0:
                raise InvalidPaymentCalculationException(f"Imposto calculado é negativo: R$ {tax:.2f}")
            if tax > gross_pay:
                raise InvalidPaymentCalculationException(
                    f"Imposto ({tax:.2f}) excede o pagamento bruto ({gross_pay:.2f})"
                )
            
            final_payment = gross_pay - tax
            if final_payment < 0:
                raise NegativePaymentException(
                    f"Pagamento final após imposto é negativo: R$ {final_payment:.2f} "
                    f"(Bruto: R$ {gross_pay:.2f}, Imposto: R$ {tax:.2f})"
                )
            
            print(f"  -> Imposto (15%): -R$ {tax:.2f}")
            return final_payment
        except (NegativePaymentException, InvalidPaymentCalculationException) as e:
            raise
        except Exception as e:
            raise InvalidPaymentCalculationException(f"Erro ao calcular desconto de imposto: {str(e)}")


class Compliance(Report):
    def __init__(self, employee: Employee):
        super().__init__(employee)
        self._violations = []
    
    def add_violation(self, date_str, description, severity):
        violation = {"Date": date_str, "Description": description, "Severity": severity}
        self._violations.append(violation)
        print(f"Violation added for {self._employee.name}")

    def remove_violation(self, index):
        try:
            if not isinstance(index, int):
                raise TypeError(f"Índice deve ser um número inteiro, recebido: {type(index).__name__}")
            if index < 0:
                raise InvalidIndexException(f"Índice não pode ser negativo, recebido: {index}")
            if len(self._violations) == 0:
                raise InvalidIndexException("Não há violações para remover")
            if index >= len(self._violations):
                raise InvalidIndexException(f"Índice {index} está fora do range. Total de violações: {len(self._violations)}")
            self._violations.pop(index)
        except (TypeError, InvalidIndexException) as e:
            raise InvalidIndexException(f"Erro ao remover violação: {str(e)}")

    def show_violations(self):
        print(f"\nCompliance Violations for {self._employee.name}:")
        if not self._violations:
            print("No violations recorded.")
        else:
            for i, v in enumerate(self._violations, 1):
                print(f"{i}) {v['Date']} - {v['Description']} | Severity: {v['Severity']}")

    # Implementação dos passos do Template Method
    def _generate_header(self) -> str:
        return f"Relatório de Compliance para {self._employee.name}"

    def _generate_body(self) -> str:
        if not self._violations:
            return "Nenhuma violação registrada."
        
        body_str = f"Total de Violações: {len(self._violations)}\n"
        for v in self._violations:
            body_str += f" - {v['Date']} | {v['Description']} (Gravidade: {v['Severity']})\n"
        return body_str