# main.py

from facade import HRFacade
from models import Observer, Employee, Department, OrganizationalComponent
from hr_system import HRSystem
from commands import AddTrainingCommand, AddPerformanceEvaluationCommand, CommandInvoker

class PayrollNotifier(Observer):
    """ Um Observer que reage a mudanças no salário de um funcionário. """
    def update(self, subject: Employee):
        print(f"\n--- ATENÇÃO PAYROLL ---")
        print(f"O salário de '{subject.name}' foi alterado para R$ {subject.salary_per_hour}/hora.")
        print(f"Por favor, atualize os registros da folha de pagamento.")
        print(f"----------------------")


def setup_organization(facade: HRFacade) -> Department:
    """
    Função auxiliar para montar a hierarquia da empresa
    usando o padrão Composite.
    """
    engineering_dept = Department("Engenharia")
    hr_dept = Department("Recursos Humanos")
    network_team = Department("Time de Redes")
    hardware_team = Department("Time de Hardware")

    marcela = facade.hire_employee(1, "Marcela Rocha", 19, "marcela@email.com", "Sistemas Embarcados", "Especialista em Hardware", 50, "2023")
    fernando = facade.hire_employee(2, "Fernando Emídio", 21, "fernando@email.com", "Redes de Computadores", "Gerente", 60, "2024")
    david = facade.hire_employee(3, "David Kelve", 20, "david@email.com", "Recursos Humanos", "Estagiário", 20, "2025")
    
    hardware_team.add_component(marcela)
    network_team.add_component(fernando)
    hr_dept.add_component(david)
    
    engineering_dept.add_component(hardware_team)
    engineering_dept.add_component(network_team)
    
    company_root = Department("Empresa X")
    company_root.add_component(engineering_dept)
    company_root.add_component(hr_dept)
    
    return company_root, marcela

def main():
    """
    Função principal que executa o loop da aplicação.
    Agora, o 'main' interage principalmente com a 'HRFacade'.
    """

    hr_facade = HRFacade()
    
    company, marcela = setup_organization(hr_facade)

    payroll_system = PayrollNotifier()
    marcela.attach(payroll_system)

    print("\n>>> MUDANDO O SALÁRIO DA MARCELA PARA DEMONSTRAR O OBSERVER <<<")
    marcela.salary_per_hour = 55 

    while True:
        print("\n============== Human Resources Management System (Facade) ==============\n")
        print("Choose your action: ")
        print("(1) Employees Data\n(2) Management\n(3) Payment\n(4) Reports\n(5) Show Company Hierarchy\n(6) Exit")

        try:
            chose = int(input("Enter your choice: "))
            
            employees = hr_facade.get_employee_list()

            match chose:
                case 1:
                    print("\n(1) Employees documentation\n(2) Add a new employee\n(3) Remove an Employee")
                    chose_1 = int(input("Choose action: "))
                    
                    match chose_1:
                        case 1:
                            print("\n--- All Employees ---")
                            if not employees:
                                print("Nenhum funcionário cadastrado.")
                            for employee in employees:
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

                            hr_facade.hire_employee(emp_type, name, age, email, department, work_position, salary, hire_date)
                            print("!! ATENÇÃO: Hierarquia da empresa precisa ser atualizada manualmente (reinicie o app) !!")

                        case 3:
                            print("\n--- Remove Employee ---")
                            for i, emp in enumerate(employees):
                                print(f"({i+1}) {emp.name}")
                            remove_index = int(input("Enter the number of the employee to remove: ")) - 1
                            
                            hr_facade.remove_employee(remove_index)
                            print("!! ATENÇÃO: Hierarquia da empresa precisa ser atualizada manualmente (reinicie o app) !!")

                case 2:
                    print("\n--- Management ---")
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    mgmt_index = int(input("Choose employee to manage: ")) - 1
                    
                    if 0 <= mgmt_index < len(employees):
                        employee = employees[mgmt_index]
                        
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
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    
                    person_index = int(input("Choose employee to calculate salary: ")) - 1
                    
                    try:
                        hr_facade.calculate_payment(person_index)
                    except Exception as e:
                        print(f"Erro ao calcular pagamento: {e}")

                case 4:
                    print("\n--- Generate Reports ---")
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    
                    rep_index = int(input("Choose employee for report: ")) - 1
                    
                    print("\n(1) Attendance Report\n(2) Compliance Report")
                    report_type = int(input("Choose report type: "))

                    try:
                        if report_type == 1:
                            hr_facade.generate_attendance_report(rep_index)
                        elif report_type == 2:
                            hr_facade.generate_compliance_report(rep_index)
                        else:
                            print("Invalid report type.")
                    except Exception as e:
                        print(f"Erro ao gerar relatório: {e}")

                case 5:
                    print("\n--- Company Organizational Hierarchy ---")
                    company.display_hierarchy()

                case 6:
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