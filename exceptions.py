# exceptions.py

class HRSystemException(Exception):
    """Exceção base para o sistema de RH."""
    pass

class EmployeeNotFoundException(HRSystemException):
    """Exceção lançada quando um funcionário não é encontrado."""
    pass

class InvalidEmployeeIndexException(HRSystemException):
    """Exceção lançada quando um índice de funcionário é inválido."""
    pass

class InvalidEmployeeDataException(HRSystemException):
    """Exceção lançada quando os dados do funcionário são inválidos."""
    pass

class InvalidNameException(InvalidEmployeeDataException):
    """Exceção lançada quando o nome é inválido."""
    pass

class InvalidAgeException(InvalidEmployeeDataException):
    """Exceção lançada quando a idade é inválida."""
    pass

class InvalidEmailException(InvalidEmployeeDataException):
    """Exceção lançada quando o email é inválido."""
    pass

class InvalidDepartmentException(InvalidEmployeeDataException):
    """Exceção lançada quando o departamento é inválido."""
    pass

class InvalidSalaryException(InvalidEmployeeDataException):
    """Exceção lançada quando o salário é inválido."""
    pass

class InvalidEmployeeTypeException(HRSystemException):
    """Exceção lançada quando o tipo de funcionário é inválido."""
    pass

class InvalidIndexException(HRSystemException):
    """Exceção lançada quando um índice genérico é inválido."""
    pass

class AttendanceException(HRSystemException):
    """Exceção base para operações de frequência."""
    pass

class ClockInWithoutClockOutException(AttendanceException):
    """Exceção lançada ao tentar fazer clock in sem ter feito clock out."""
    pass

class ClockOutWithoutClockInException(AttendanceException):
    """Exceção lançada ao tentar fazer clock out sem ter feito clock in."""
    pass

class NoAttendanceRecordsException(AttendanceException):
    """Exceção lançada quando não há registros de frequência."""
    pass

class PaymentException(HRSystemException):
    """Exceção base para operações de pagamento."""
    pass

class InvalidPaymentCalculationException(PaymentException):
    """Exceção lançada quando há erro no cálculo de pagamento."""
    pass

class NegativePaymentException(PaymentException):
    """Exceção lançada quando o pagamento calculado é negativo."""
    pass

class InvalidDateException(HRSystemException):
    """Exceção lançada quando uma data é inválida."""
    pass

class InvalidTimeException(HRSystemException):
    """Exceção lançada quando um horário é inválido."""
    pass

class InvalidPerformanceLevelException(HRSystemException):
    """Exceção lançada quando o nível de performance é inválido."""
    pass

class BenefitAlreadyExistsException(HRSystemException):
    """Exceção lançada quando tenta adicionar um benefício que já existe."""
    pass

class BenefitNotFoundException(HRSystemException):
    """Exceção lançada quando um benefício não é encontrado."""
    pass

class ListSynchronizationException(HRSystemException):
    """Exceção lançada quando as listas do sistema estão dessincronizadas."""
    pass

