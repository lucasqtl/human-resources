# services.py

from datetime import datetime
from abc import ABC, abstractmethod
from models import Employee

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
        now = datetime.now()
        self._record.append({"in": now, "out": None})
        print(f"{self._employee.name} clocked in at {now.strftime('%H:%M:%S')}")
    
    def clock_out(self):
        now = datetime.now()
        if self._record and self._record[-1]["out"] is None:
            self._record[-1]["out"] = now
            print(f"{self._employee.name} clocked out at {now.strftime('%H:%M:%S')}")
        else:
            print("You need to clock in before clocking out.")
    
    def show_records(self):
        print(f"\nRecords of {self._employee.name}: ")
        for i, record in enumerate(self._record, 1):
            in_time = record['in'].strftime('%Y-%m-%d %H:%M:%S')
            out_time = record['out'].strftime('%Y-%m-%d %H:%M:%S') if record['out'] else "Still working"
            print(f"{i}) IN: {in_time} | OUT: {out_time}")

    def worked_hours_per_day(self):
        print(f"\nWorked hours for {self._employee.name}:")
        total_seconds = 0
        for record in self._record:
            if record["out"] is not None:
                worked = record["out"] - record["in"]
                total_seconds += worked.total_seconds()
                print(f"- {record['in'].strftime('%Y-%m-%d')}: {worked}")
        
        total_hours = total_seconds // 3600
        total_minutes = (total_seconds % 3600) // 60
        print(f"\nTotal worked time: {int(total_hours)}h {int(total_minutes)}min\n")
    

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
        total_seconds = 0
        for record in attendance._record:
            if record["in"] and record["out"]:
                worked = record["out"] - record["in"]
                total_seconds += worked.total_seconds()
        total_hours = total_seconds / 3600
        return total_hours * salary_per_hour

class MonthlyPaymentStrategy(PaymentStrategy):
    """ Estratégia Concreta: Calcula um pagamento fixo mensal (ex: 160 horas de trabalho). """
    def calculate(self, attendance: Attendance, salary_per_hour: float) -> float:
        FIXED_HOURS_PER_MONTH = 160
        return FIXED_HOURS_PER_MONTH * salary_per_hour

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


class Compliance(Report):
    def __init__(self, employee: Employee):
        super().__init__(employee)
        self._violations = []
    
    def add_violation(self, date_str, description, severity):
        violation = {"Date": date_str, "Description": description, "Severity": severity}
        self._violations.append(violation)
        print(f"Violation added for {self._employee.name}")

    def remove_violation(self, index):
        if 0 <= index < len(self._violations):
            self._violations.pop(index)
        else:
            print("Invalid index")

    def show_violations(self):
        print(f"\nCompliance Violations for {self._employee.name}:")
        if not self._violations:
            print("No violations recorded.")
        else:
            for i, v in enumerate(self._violations, 1):
                print(f"{i}) {v['Date']} - {v['Description']} | Severity: {v['Severity']}")

    def _generate_header(self) -> str:
        return f"Relatório de Compliance para {self._employee.name}"

    def _generate_body(self) -> str:
        if not self._violations:
            return "Nenhuma violação registrada."
        
        body_str = f"Total de Violações: {len(self._violations)}\n"
        for v in self._violations:
            body_str += f" - {v['Date']} | {v['Description']} (Gravidade: {v['Severity']})\n"
        return body_str



