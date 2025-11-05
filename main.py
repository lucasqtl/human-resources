# main.py

from facade import HRFacade
from models import Observer, Employee, Department, OrganizationalComponent
from hr_system import HRSystem
from commands import AddTrainingCommand, AddPerformanceEvaluationCommand, CommandInvoker
from exceptions import (
    InvalidEmployeeIndexException, InvalidEmployeeDataException,
    InvalidEmployeeTypeException, InvalidIndexException,
    InvalidPerformanceLevelException, HRSystemException
)

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
            try:
                chose = int(input("Enter your choice: "))
            except ValueError:
                raise ValueError("Por favor, digite um número válido para a opção do menu")
            
            employees = hr_facade.get_employee_list()

            match chose:
                case 1:
                    print("\n(1) Employees documentation\n(2) Add a new employee\n(3) Remove an Employee")
                    try:
                        chose_1 = int(input("Choose action: "))
                    except ValueError:
                        print("Erro: Por favor, digite um número válido para a ação")
                        continue
                    
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
                            try:
                                name = input("Name: ")
                                if not name or len(name.strip()) == 0:
                                    print("Erro: Nome não pode ser vazio")
                                    continue
                                
                                try:
                                    age = int(input("Age: "))
                                except ValueError:
                                    print("Erro: Idade deve ser um número inteiro")
                                    continue
                                
                                email = input("Email: ")
                                if not email or len(email.strip()) == 0:
                                    print("Erro: Email não pode ser vazio")
                                    continue
                                
                                department = input("Department: ")
                                if not department or len(department.strip()) == 0:
                                    print("Erro: Departamento não pode ser vazio")
                                    continue
                                
                                work_position = input("Work Position: ")
                                
                                try:
                                    salary = float(input("Salary per hour: "))
                                except ValueError:
                                    print("Erro: Salário deve ser um número válido")
                                    continue
                                
                                hire_date = input("Hire Date (YYYY): ")
                                
                                try:
                                    emp_type = int(input("Employee Type (1: Regular, 2: Manager, 3: Intern): "))
                                    if emp_type not in [1, 2, 3]:
                                        print("Erro: Tipo de funcionário deve ser 1, 2 ou 3")
                                        continue
                                except ValueError:
                                    print("Erro: Tipo de funcionário deve ser um número inteiro (1, 2 ou 3)")
                                    continue
                                
                                hr_facade.hire_employee(emp_type, name, age, email, department, work_position, salary, hire_date)
                                print("!! ATENÇÃO: Hierarquia da empresa precisa ser atualizada manualmente (reinicie o app) !!")
                            except (InvalidEmployeeDataException, InvalidEmployeeTypeException) as e:
                                print(f"Erro ao criar funcionário: {str(e)}")
                            except HRSystemException as e:
                                print(f"Erro no sistema: {str(e)}")

                        case 3:
                            print("\n--- Remove Employee ---")
                            if not employees:
                                print("Nenhum funcionário cadastrado para remover")
                                continue
                            
                            for i, emp in enumerate(employees):
                                print(f"({i+1}) {emp.name}")
                            
                            try:
                                remove_index = int(input("Enter the number of the employee to remove: ")) - 1
                                if remove_index < 0 or remove_index >= len(employees):
                                    print(f"Erro: Índice inválido. Escolha um número entre 1 e {len(employees)}")
                                    continue
                            except ValueError:
                                print("Erro: Por favor, digite um número válido")
                                continue
                            
                            try:
                                hr_facade.remove_employee(remove_index)
                                print("!! ATENÇÃO: Hierarquia da empresa precisa ser atualizada manualmente (reinicie o app) !!")
                            except InvalidEmployeeIndexException as e:
                                print(f"Erro ao remover funcionário: {str(e)}")
                            except HRSystemException as e:
                                print(f"Erro no sistema: {str(e)}")

                case 2:
                    print("\n--- Management ---")
                    if not employees:
                        print("Nenhum funcionário cadastrado para gerenciar")
                        continue
                    
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    
                    try:
                        mgmt_index = int(input("Choose employee to manage: ")) - 1
                        if mgmt_index < 0 or mgmt_index >= len(employees):
                            print(f"Erro: Índice inválido. Escolha um número entre 1 e {len(employees)}")
                            continue
                    except ValueError:
                        print("Erro: Por favor, digite um número válido")
                        continue
                    
                    employee = employees[mgmt_index]
                    
                    print(f"\nManaging {employee.name}:")
                    print("(1) Add Training\n(2) Add Performance Evaluation\n(3) Show Data")
                    
                    try:
                        action = int(input("Choose action: "))
                    except ValueError:
                        print("Erro: Por favor, digite um número válido para a ação")
                        continue
                    
                    try:
                        if action == 1:
                            date = input("Training Date (YYYY-MM-DD): ")
                            time = input("Time (HH:MM): ")
                            desc = input("Description: ")
                            if not desc or len(desc.strip()) == 0:
                                print("Erro: Descrição não pode ser vazia")
                                continue
                            command = AddTrainingCommand(employee, date, time, desc)
                            invoker = CommandInvoker(command)
                            invoker.run()

                        elif action == 2:
                            print("Performance Level (1: Good, 2: Average, 3: Bad)")
                            try:
                                level = int(input("Choose level: "))
                                if level not in [1, 2, 3]:
                                    print("Erro: Nível deve ser 1, 2 ou 3")
                                    continue
                            except ValueError:
                                print("Erro: Nível deve ser um número inteiro (1, 2 ou 3)")
                                continue
                            command = AddPerformanceEvaluationCommand(employee, level)
                            invoker = CommandInvoker(command)
                            invoker.run()

                        elif action == 3:
                            employee.show_training()
                            employee.show_performance()
                        else:
                            print("Ação inválida. Escolha 1, 2 ou 3")
                    except InvalidPerformanceLevelException as e:
                        print(f"Erro ao processar comando: {str(e)}")
                    except HRSystemException as e:
                        print(f"Erro no sistema: {str(e)}")

                case 3:
                    print("\n--- Calculate Payment ---")
                    if not employees:
                        print("Nenhum funcionário cadastrado para calcular pagamento")
                        continue
                    
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    
                    try:
                        person_index = int(input("Choose employee to calculate salary: ")) - 1
                        if person_index < 0 or person_index >= len(employees):
                            print(f"Erro: Índice inválido. Escolha um número entre 1 e {len(employees)}")
                            continue
                    except ValueError:
                        print("Erro: Por favor, digite um número válido")
                        continue
                    
                    try:
                        hr_facade.calculate_payment(person_index)
                    except InvalidEmployeeIndexException as e:
                        print(f"Erro ao calcular pagamento: {str(e)}")
                    except HRSystemException as e:
                        print(f"Erro no sistema: {str(e)}")

                case 4:
                    print("\n--- Generate Reports ---")
                    if not employees:
                        print("Nenhum funcionário cadastrado para gerar relatório")
                        continue
                    
                    for i, emp in enumerate(employees):
                        print(f"({i+1}) {emp.name}")
                    
                    try:
                        rep_index = int(input("Choose employee for report: ")) - 1
                        if rep_index < 0 or rep_index >= len(employees):
                            print(f"Erro: Índice inválido. Escolha um número entre 1 e {len(employees)}")
                            continue
                    except ValueError:
                        print("Erro: Por favor, digite um número válido")
                        continue
                    
                    print("\n(1) Attendance Report\n(2) Compliance Report")
                    try:
                        report_type = int(input("Choose report type: "))
                        if report_type not in [1, 2]:
                            print("Erro: Tipo de relatório deve ser 1 ou 2")
                            continue
                    except ValueError:
                        print("Erro: Por favor, digite um número válido (1 ou 2)")
                        continue

                    try:
                        if report_type == 1:
                            hr_facade.generate_attendance_report(rep_index)
                        elif report_type == 2:
                            hr_facade.generate_compliance_report(rep_index)
                    except InvalidEmployeeIndexException as e:
                        print(f"Erro ao gerar relatório: {str(e)}")
                    except HRSystemException as e:
                        print(f"Erro no sistema: {str(e)}")

                case 5:
                    print("\n--- Company Organizational Hierarchy ---")
                    company.display_hierarchy()

                case 6:
                    print("Exiting system. Goodbye!")
                    return

                case _:
                    print("Invalid option, please try again.")

        except ValueError as e:
            print(f"\nErro: Entrada inválida. {str(e)}")
        except KeyboardInterrupt:
            print("\n\nOperação cancelada pelo usuário. Encerrando...")
            return
        except HRSystemException as e:
            print(f"\nErro no sistema de RH: {str(e)}")
        except Exception as e:
            print(f"\nErro inesperado: {str(e)}")
            print("Por favor, tente novamente ou reinicie o sistema.")

if __name__ == "__main__":
    main()