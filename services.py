# services.py
from datetime import datetime
from abc import ABC, abstractmethod
from models import Employee  # Importamos a classe Employee do nosso outro arquivo

class Report(ABC):
    """
    Classe Abstrata para servir de modelo para qualquer tipo de relatório.
    """
    def __init__(self, employee: Employee):
        self._employee = employee
    
    @abstractmethod
    def generate_report(self):
        pass

class Attendance(Report):
    """
    Controla o registro de ponto (entrada e saída) de um funcionário.
    """
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
    
    def generate_report(self):
        self.show_records()

class PaymentCalculator(ABC):
    """
    Classe Abstrata para calculadoras de pagamento.
    """
    def __init__(self, attendance: Attendance, salary_per_hour: float):
        self._attendance = attendance
        self._salary_per_hour = salary_per_hour
    
    @abstractmethod
    def calculate_payment(self):
        pass

class Payment(PaymentCalculator):
    """
    Implementação concreta que calcula o pagamento com base nas horas trabalhadas.
    """
    def calculate_payment(self):
        total_seconds = 0
        for record in self._attendance._record:
            if record["in"] and record["out"]:
                worked = record["out"] - record["in"]
                total_seconds += worked.total_seconds()
        total_hours = total_seconds / 3600
        pay = total_hours * self._salary_per_hour
        return pay

class Compliance(Report):
    """
    Gerencia violações de conformidade de um funcionário.
    """
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

    def generate_report(self):
        print(f"\nCompliance Report for {self._employee.name}")
        print(f"Number of Violations: {len(self._violations)}")
        if self._violations:
            for v in self._violations:
                print(f" - {v['Date']} | {v['Description']} (Severity: {v['Severity']})")