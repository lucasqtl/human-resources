# main.py
from services import PaymentContext, HourlyPaymentStrategy, MonthlyPaymentStrategy
from models import Observer, Employee
from factories import EmployeeFactory
from hr_system import HRSystem
from commands import AddTrainingCommand, AddPerformanceEvaluationCommand, CommandInvoker

class PayrollNotifier(Observer):
    """ Um Observer que reage a mudanças no salário de um funcionário. """
    def update(self, subject: Employee):
        print(f"\n--- ATENÇÃO PAYROLL ---")
        print(f"O salário de '{subject.name}' foi alterado para R$ {subject.salary_per_hour}/hora.")
        print(f"Por favor, atualize os registros da folha de pagamento.")
        print(f"----------------------")

def load_initial_data(hr_system):
    """
    Função auxiliar para popular o sistema com dados iniciais,
    demonstrando o uso da Factory e do Singleton juntos.
    """
    print("Loading initial employee data...")
    initial_employees_data = [
        (1, "Marcela Rocha", 19, "marcela@email.com", "Sistemas Embarcados", "Especialista em Hardware", 50, "2023"),
        (2, "Fernando Emídio", 21, "fernando@email.com", "Redes de Computadores", "Gerente", 60, "2024"),
        (3, "David Kelve", 20, "david@email.com", "Recursos Humanos", "Estagiário", 20, "2025")
    ]

    for data in initial_employees_data:
        employee = EmployeeFactory.create_employee(*data)
        hr_system.add_employee(employee)

def main():
    """
    Função principal que executa o loop da aplicação.
    O estado da aplicação é gerenciado pelo Singleton HRSystem.
    """
    hr = HRSystem.get_instance()
    load_initial_data(hr)

    payroll_system = PayrollNotifier()
    marcela = hr.employees_list[0]
    marcela.attach(payroll_system)

    print("\n>>> MUDANDO O SALÁRIO DA MARCELA PARA DEMONSTRAR O OBSERVER <<<")
    marcela.salary_per_hour = 55

    while True:
        print("\n============== Human Resources Management System ==============\n")
        print("Choose your action: ")
        print("(1) Employees Data\n(2) Management\n(3) Payment\n(4) Reports\n(5) Exit") # Renomeado para Reports

        try:
            chose = int(input("Enter your choice: "))

            match chose:
                case 1:
                    print("\n(1) Employees documentation\n(2) Add a new employee\n(3) Modify employee data\n(4) Remove an Employee\n(5) Benefits management")
                    chose_1 = int(input("Choose action: "))
                    
                    match chose_1:
                        case 1:
                            print("\n--- All Employees ---")
                            for employee in hr.employees_list:
                                employee.display_info()
                                print(f"Role: {employee.get_role()}\n")
                        
                        case 2:
                            print("\nPlease provide new employee details:")
                            name = input("Name: ")
                            age = int(input("Age: "))
                            email = input("Email: ")
                            department = input("Department: ")
                            work_position = input("Work Position: ")
                            salary = float(input("Salary per hour: "))
                            hire_date = input("Hire Date (YYYY): ")
                            emp_type = int(input("Employee Type (1: Regular, 2: Manager, 3: Intern): "))

                            new_employee = EmployeeFactory.create_employee(emp_type, name, age, email, department, work_position, salary, hire_date)
                            hr.add_employee(new_employee)
                            print("Employee added successfully!")

                        case 3:
                            print("\n--- Modify Employee ---")
                            for i, emp in enumerate(hr.employees_list):
                                print(f"({i+1}) {emp.name}")
                            mod_index = int(input("Choose employee to modify: ")) - 1
                            if 0 <= mod_index < len(hr.employees_list):
                                print(f"Modifying {hr.employees_list[mod_index].name}...")
                            else:
                                print("Invalid index.")
                        
                        case 4:
                            print("\n--- Remove Employee ---")
                            for i, emp in enumerate(hr.employees_list):
                                print(f"({i+1}) {emp.name}")
                            remove_index = int(input("Enter the number of the employee to remove: ")) - 1
                            hr.remove_employee(remove_index)

                        case 5:
                            print("\n--- Manage Benefits ---")
                            for i, emp in enumerate(hr.employees_list):
                                print(f"({i+1}) {emp.name}")
                            ben_index = int(input("Choose employee: ")) - 1
                            if 0 <= ben_index < len(hr.employees_list):
                                print(f"Managing benefits for {hr.employees_list[ben_index].name}...")
                            else:
                                print("Invalid index.")
                case 2:
                    print("\n--- Management ---")
                    for i, emp in enumerate(hr.employees_list):
                        print(f"({i+1}) {emp.name}")
                    mgmt_index = int(input("Choose employee to manage: ")) - 1
                    
                    if 0 <= mgmt_index < len(hr.employees_list):
                        employee = hr.employees_list[mgmt_index]
                        
                        print(f"\nManaging {employee.name}:")
                        print("(1) Add Training\n(2) Add Performance Evaluation\n(3) Show Data")
                        action = int(input("Choose action: "))

                        if action == 1:
                            date = input("Training Date (YYYY-MM-DD): ")
                            time = input("Time (HH:MM): ")
                            desc = input("Description: ")
                            command = AddTrainingCommand(employee, date, time, desc)
                            invoker = CommandInvoker(command)
                            invoker.run()

                        elif action == 2:
                            print("Performance Level (1: Good, 2: Average, 3: Bad)")
                            level = int(input("Choose level: "))
                            command = AddPerformanceEvaluationCommand(employee, level)
                            invoker = CommandInvoker(command)
                            invoker.run()

                        elif action == 3:
                            employee.show_training()
                            employee.show_performance()
                    else:
                        print("Invalid index.")

                case 3:
                    print("\n--- Calculate Payment ---")
                    for i, emp in enumerate(hr.employees_list):
                        print(f"({i+1}) {emp.name}")
                    
                    person_index = int(input("Choose employee to calculate salary: ")) - 1
                    
                    if 0 <= person_index < len(hr.employees_list):
                        employee = hr.employees_list[person_index]
                        attendance = hr.attendance_list[person_index]

                        strategy = HourlyPaymentStrategy()
                        payment_context = PaymentContext(strategy)
                        money = payment_context.calculate_payment(attendance, employee.salary_per_hour)
                        
                        print(f"\nTotal payment for {employee.name}: R$ {money:.2f}")
                    else:
                        print("Invalid index.")
                case 4:
                    print("\n--- Generate Reports ---")
                    for i, emp in enumerate(hr.employees_list):
                        print(f"({i+1}) {emp.name}")
                    
                    rep_index = int(input("Choose employee for report: ")) - 1
                    
                    if 0 <= rep_index < len(hr.employees_list):
                        print("\n(1) Attendance Report\n(2) Compliance Report")
                        report_type = int(input("Choose report type: "))

                        if report_type == 1:
                            attendance_report = hr.attendance_list[rep_index]
                            attendance_report.generate_report()
                        elif report_type == 2:
                            compliance_report = hr.compliance_list[rep_index]
                            compliance_report.generate_report()
                        else:
                            print("Invalid report type.")
                    else:
                        print("Invalid index.")

                case 5:
                    print("Exiting system. Goodbye!")
                    return

                case _:
                    print("Invalid option, please try again.")

        except ValueError:
            print("\nError: Invalid input. Please enter a number where required.")
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    main()