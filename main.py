# main.py
from services import PaymentContext, HourlyPaymentStrategy, MonthlyPaymentStrategy
from models import Observer, Employee
from factories import EmployeeFactory
from hr_system import HRSystem

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
    # Dados no formato: (type, name, age, email, dept, position, salary, hire_date)
    initial_employees_data = [
        (1, "Marcela Rocha", 19, "marcela@email.com", "Sistemas Embarcados", "Especialista em Hardware", 50, "2023"),
        (2, "Fernando Emídio", 21, "fernando@email.com", "Redes de Computadores", "Gerente", 60, "2024"),
        (3, "David Kelve", 20, "david@email.com", "Recursos Humanos", "Estagiário", 20, "2025")
    ]

    for data in initial_employees_data:
        employee = EmployeeFactory.create_employee(*data)
        hr_system.add_employee(employee) # Adiciona através do Singleton

def main():
    """
    Função principal que executa o loop da aplicação.
    O estado da aplicação é gerenciado pelo Singleton HRSystem.
    """
    # Ponto de acesso global ao nosso sistema de RH
    hr = HRSystem.get_instance()
    load_initial_data(hr)

    # Criando e anexando o observer para demonstração
    payroll_system = PayrollNotifier()
    marcela = hr.employees_list[0]
    marcela.attach(payroll_system)

    print("\n>>> MUDANDO O SALÁRIO DA MARCELA PARA DEMONSTRAR O OBSERVER <<<")
    marcela.salary_per_hour = 55 # Esta ação vai automaticamente disparar a notificação

    while True:
        print("\n============== Human Resources Management System ==============\n")
        print("Choose your action: ")
        print("(1) Employees Data\n(2) Management\n(3) Payment\n(4) Compliance Report\n(5) Exit")

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
                                # A lógica de modificação detalhada pode ser adicionada aqui
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
                                # A lógica de benefícios detalhada pode ser adicionada aqui
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
                        attendance = hr.attendance_list[mgmt_index]
                        
                        print(f"\nManaging {employee.name}:")
                        print("(1) Time tracking\n(2) Performance\n(3) Training")
                        action = int(input("Choose action: "))
                        if action == 1:
                            attendance.show_records()
                        elif action == 2:
                            employee.show_performance()
                        elif action == 3:
                            employee.show_training()
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

                        # Usando o padrão Strategy corretamente
                        strategy = HourlyPaymentStrategy()
                        payment_context = PaymentContext(strategy)
                        money = payment_context.calculate_payment(attendance, employee.salary_per_hour)
                        
                        print(f"\nTotal payment for {employee.name}: R$ {money:.2f}")
                    else:
                        print("Invalid index.")

                case 4:
                    print("\n--- Compliance Report ---")
                    for i, emp in enumerate(hr.employees_list):
                        print(f"({i+1}) {emp.name}")
                    
                    comp_index = int(input("Choose employee for compliance report: ")) - 1
                    
                    if 0 <= comp_index < len(hr.employees_list):
                        compliance = hr.compliance_list[comp_index]
                        compliance.generate_report()
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