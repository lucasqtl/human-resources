# main.py
from models import Employee, Manager, Intern
from services import Attendance, Payment, Compliance

def main():
    """
    Função principal que executa o loop da aplicação.
    """
    # Dados iniciais
    employee_1 = Employee("Marcela Rocha", 19, "Marcela_2023@gmail.com", "Sistemas embarcados", "Especialista em Hardware", 50, 2023)
    employee_2 = Manager("Fernando Emídio", 21, "Fe_Emi@gmail.com", "Redes de computadores", 60, 2024)
    employee_3 = Intern("David Kelve", 20, "dkob@ic.ufal.br", "Recursos humanos", 20, 2025)

    employees_list = [employee_1, employee_2, employee_3]
    
    # Cada funcionário tem seu próprio serviço de attendance e compliance
    attendance_list = [Attendance(emp) for emp in employees_list]
    compliance_list = [Compliance(emp) for emp in employees_list]

    while True:
        print("============== Human Resources Management System ==============\n")
        print("Choose your action: ")
        print("(1) Employees Data\n(2) Management\n(3) Payment\n(4) Compliance Report\n(5) Exit")

        try:
            chose = int(input())

            match chose:
                case 1:
                    print("Choose your action: ")
                    print("(1) Employees documentation\n(2) Add a new employee\n(3) Employees modify\n(4) Remove an Employee\n(5) Benefits management ")
                    chose_1 = int(input())
                    
                    match chose_1:
                        case 1: 
                            print("\n")
                            for employee in employees_list:
                                employee.display_info() 
                                print(f"Role: {employee.get_role()}")  
                                print("\n")
                            print(f"Number of employees: {Employee.number_of_employees}")
                        
                        case 2: 
                            print("Please, right below add the new employee documentation!")

                            while True:
                                    try:
                                        name = input("Name: ")
                                        try:
                                            age = int(input("Age: "))
                                        except ValueError:
                                            print("Age must be a number. Please try again.")
                                            continue
                                        
                                        email = input("Email: ")
                                        department = input("Department: ")
                                        work_position = input("Work Position: ")
                                    
                                        try:
                                            salary = float(input("Salary per hours: "))
                                        except ValueError:
                                            print("Salary must be a number. Please try again.")
                                            continue
                                        
                                        hire_date = input("Hire Date: ")
                                        
                                        print("Employee Type: (1) Regular Employee (2) Manager (3) Intern")
                                        try:
                                            emp_type = int(input("Choose type: "))
                                        except ValueError:
                                            print("Invalid type, creating regular employee")
                                            emp_type = 1
                                        
                                        try:
                                            if emp_type == 1:
                                                new_employee = Employee(name, age, email, department, work_position, salary, hire_date)
                                            elif emp_type == 2:
                                                new_employee = Manager(name, age, email, department, salary, hire_date)
                                            elif emp_type == 3:
                                                new_employee = Intern(name, age, email, department, salary, hire_date)
                                            else:
                                                print("Invalid type, creating regular employee")
                                                new_employee = Employee(name, age, email, department, work_position, salary, hire_date)

                                            employees_list.append(new_employee)
                                            attendance_list.append(Attendance(new_employee))
                                            compliance_list.append(Compliance(new_employee))

                                            print("\nEmployee successfully added!")
                                            print(f"Number of employees: {Employee.number_of_employees}")
                                            
                                            again = input("Do you want to add another employee? (y/n) ").lower()
                                            if again != 'y':
                                                break
                                        
                                        except ValueError as e:

                                            print(f"Validation error: {e}")
                                            print("Please try again with correct data.")
                                            continue
                                            
                                    except KeyboardInterrupt:
                                        print("\nOperation cancelled by user.")
                                        break
                                    except Exception as e:
                                        print(f"Unexpected error: {e}")
                                        continue
                        
                        case 3:
                            while True:
                                j = 1
                                print("Employees list")
                                for employee in employees_list:
                                    print(f"({j}) {employee.name}")
                                    j += 1
                                try:
                                    mod = int(input("Choose the employee you want to modify: "))
                                    if 1 <= mod <= len(employees_list):
                                        chosen_one = employees_list[mod-1]

                                        types_of_data = {
                                            1: "name",
                                            2: "age", 
                                            3: "email",
                                            4: "department",
                                            5: "work_position",
                                            6: "salary_per_hour",
                                            7: "hire_date"
                                        }
                                        
                                        print("(1) Name || (2) Age || (3) Email || (4) Department || (5) Work Position || (6) Salary per hours || (7) Hire Date")
                                        data = int(input("Choose data you want to modify: "))
                                        
                                        if data in types_of_data:
                                            new_value = input(f"Enter the new data for {types_of_data[data]}: ")
                                            if types_of_data[data] in ["age", "salary_per_hour"]:
                                                new_value = float(new_value) if types_of_data[data] == "salary_per_hour" else int(new_value)

                                            if types_of_data[data] == "name":
                                                chosen_one.name = new_value

                                            elif types_of_data[data] == "age":
                                                chosen_one.age = new_value
                                            elif types_of_data[data] == "email":
                                                chosen_one.email = new_value

                                            elif types_of_data[data] == "department":
                                                chosen_one.department = new_value

                                            elif types_of_data[data] == "work_position":
                                                chosen_one.work_position = new_value
                                            elif types_of_data[data] == "salary_per_hour":
                                                chosen_one.salary_per_hour = new_value
                                                
                                            elif types_of_data[data] == "hire_date":
                                                chosen_one.hire_date = new_value
                                            
                                            print(f"{types_of_data[data]} was modified successfully")
                                        else:
                                            print("Invalid data option")

                                        loop = input("Do you want to modify some attribute again (y/n)? ")
                                        if loop != 'y':
                                            break
                                    else:
                                        print("Invalid employee number\n")
                                        
                                except (ValueError, Exception) as e:
                                    print(f"Error: {e}")
                        
                        case 4: 
                            while True:
                                if len(employees_list) == 0:
                                    print("There's nothing here")
                                    break
                                
                                i = 1
                                print("Employees list")
                                for employee in employees_list:
                                    print(f"({i}) {employee.name}")
                                    i += 1
                                
                                try:
                                    remove_index = int(input("Enter the number of the employee to remove: "))
                                    if 1 <= remove_index <= len(employees_list):
                                        removed = employees_list.pop(remove_index-1)
                                        attendance_list.pop(remove_index-1)
                                        compliance_list.pop(remove_index-1)
                                        Employee.number_of_employees -= 1
                                        print(f"{removed.name} has been removed from the system.\n")
                                    else:
                                        print("Invalid employee number\n")
                                except ValueError:
                                    print("Invalid input. Please enter a number.\n")

                                again = input("Do you want to remove another employee? (y/n) ").lower()
                                if again != 'y':
                                    break
                        
                        case 5: 
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            try:
                                chosen = int(input("Choose an employee: "))-1
                                if 0 <= chosen < len(employees_list):
                                    chosen_one = employees_list[chosen]
                                    print(f"Managing benefits of {chosen_one.name}")
                                    print("(1) Add benefit\n(2) Remove benefit\n(3) Show benefits")
                                    
                                    act = int(input("Choose your action: "))

                                    if act == 1:
                                        benefit = input("Enter the benefit to add: ")
                                        chosen_one.add_benefit(benefit)
                                    elif act == 2:
                                        benefit = input("Enter the benefit to remove: ")
                                        chosen_one.remove_benefit(benefit)
                                    elif act == 3:
                                        print("Benefits:", ", ".join(chosen_one._benefits) if chosen_one._benefits else "None")
                                    else:
                                        print("Invalid option")
                                else:
                                    print("Invalid Employee number")

                            except ValueError:
                                print("Invalid input. Please enter a number.\n")
                        
                        case _:
                            print("Invalid option")

                case 2: 
                    print("Choose your action: ")
                    print("(1) Time tracking register\n(2) Attendance Records\n(3) Show worked hours per employee\n(4) Performance Evaluation management\n(5) Meetings\n(6) Leave request")
                    chose_2 = int(input())
                    
                    match chose_2:
                        case 1: 
                            clock = int(input("What you want to register?\n(1)Clock in\n(2)Clock out\n"))
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            try:
                                chose = int(input("Choose one employee to register: "))-1
                                if 0 <= chose < len(employees_list):
                                    chosen_one = attendance_list[chose]

                                    if clock == 1:
                                        chosen_one.clock_in()
                                    elif clock == 2:
                                        chosen_one.clock_out()
                                    else:
                                        print("Invalid option")
                                else:
                                    print("Invalid employee number")
                            except ValueError:
                                print("Invalid input. Please enter a number.\n")
                        
                        case 2:
                            for attendance in attendance_list:
                                attendance.show_records()  
                                print()
                        
                        case 3: 
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            try:
                                chose = int(input("Choose one employee to view worked hours: "))-1
                                if 0 <= chose < len(employees_list):
                                    attendance_list[chose].worked_hours_per_day()
                                else:
                                    print("Invalid employee number.\n")
                            except ValueError:
                                print("Invalid input")
                        
                        case 4: 
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                                
                            try:
                                chose = int(input())-1
                                if 0 <= chose < len(employees_list):
                                    chosen_one = employees_list[chose]
                                    print("(1) Add an evaluation\n(2) Remove an evaluation\n(3) Show the evaluation")
                                    case = int(input("Choose one index: "))
                                    
                                    if case == 1:
                                        print("Choose the evaluation level:")
                                        print("(1) Good\n(2) Average\n(3) Bad")
                                        eva = int(input("Level: "))
                                        chosen_one.add_performance_evaluation(eva)
                                    elif case == 2:
                                        chosen_one.show_performance()
                                        index = int(input("Type the number you want to remove: ")) - 1
                                        chosen_one.remove_performance_evaluation(index)
                                    elif case == 3:
                                        chosen_one.show_performance()
                                    else:
                                        print("Invalid index")
                                else:
                                    print("Invalid employee number.\n")

                            except ValueError:
                                print("Invalid input")
                        
                        case 5: 
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            try:
                                chose = int(input("Choose one employee to analyze the meeting schedule: ")) - 1
                                if 0 <= chose < len(employees_list):
                                    chosen_one = employees_list[chose]
                                    print("(1) Add a new meeting\n(2) Remove a meeting\n(3) Show the meetings")
                                    case = int(input("Choose one index: "))
                                    
                                    if case == 1:
                                        data = str(input("Date: "))
                                        temp = str(input("Hour: "))
                                        description = str(input("Description: "))
                                        chosen_one.add_training(data, temp, description)
                                    elif case == 2:
                                        chosen_one.show_training()
                                        index = int(input("Type the number you want to remove: "))-1
                                        chosen_one.remove_training(index)
                                    elif case == 3:
                                        chosen_one.show_training()
                                    else:
                                        print("Invalid index")
                                else:
                                    print("Invalid employee number.\n")

                            except ValueError:
                                print("Invalid input")
                        
                        case 6: 
                            print("Employees list")
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            try:
                                chose = int(input("Choose one employee to manage leave requests: ")) - 1
                                if 0 <= chose < len(employees_list):
                                    chosen_one = employees_list[chose]
                                    print(f"Managing leave requests for {chosen_one.name}")
                                    print("(1) Add leave request\n(2) Remove leave request\n(3) Show leave requests")
                                    action = int(input("Choose your action: "))

                                    if action == 1:
                                        start_date = input("Enter start date (e.g., 01/08): ")
                                        end_date = input("Enter end date (e.g., 05/08): ")
                                        reason = input("Enter reason: ")
                                        chosen_one.add_leave_request(start_date, end_date, reason)
                                    elif action == 2:
                                        chosen_one.show_leave_requests()
                                        index = int(input("Enter the index of the leave request to remove: ")) - 1
                                        chosen_one.remove_leave_request(index)
                                    elif action == 3:
                                        chosen_one.show_leave_requests()
                                    else:
                                        print("Invalid option")
                                else:
                                    print("Invalid employee number.")
                            except ValueError:
                                print("Invalid input. Please enter numbers.")
                        
                        case _:
                            print("Invalid option")

                case 3: 
                    print("(1) Payment without benefits")
                    chose = int(input("Choose your action: "))
                    
                    match chose:
                        case 1:
                            for i, employee in enumerate(employees_list, start=1):
                                print(f"({i}) {employee.name}")
                            person = int(input("Choose the employee you want to calculate the salary: "))-1
                            
                            try:
                                if 0 <= person < len(employees_list):
                                    employee = employees_list[person]
                                    attendance = attendance_list[person]
                                    payment = Payment(attendance, employee.salary_per_hour)  # POLIMORFISMO
                                    money = payment.calculate_payment()

                                    print(f"\nTotal payment for {employee.name}: R$ {money:.2f}\n")
                                else:
                                    print("Invalid employee number\n")
                            except ValueError:
                                print("Invalid input")
                        case _:
                            print("Invalid option")

                case 4: 
                    print("Compliance Management")
                    print("(1) Add Violation\n(2) Remove Violation\n(3) Show Violations\n(4) Generate Compliance Report")
                    action = int(input("Choose your action: "))
                    
                    print("Employees list:")
                    for i, employee in enumerate(employees_list, start=1):
                        print(f"({i}) {employee.name}")
                    
                    try:
                        chose = int(input("Choose the employee: ")) - 1

                        if 0 <= chose < len(employees_list):
                            chosen_one = compliance_list[chose]

                            if action == 1:
                                date_str = input("Enter violation date (dd/mm/yyyy): ")
                                description = input("Enter violation description: ")
                                severity = input("Enter severity (Low/Medium/High): ")
                                chosen_one.add_violation(date_str, description, severity)

                            elif action == 2:
                                chosen_one.show_violations()
                                if chosen_one._violations:
                                    index = int(input("Enter violation index to remove: ")) - 1
                                    chosen_one.remove_violation(index)

                            elif action == 3:
                                chosen_one.show_violations()

                            elif action == 4:
                                chosen_one.generate_report() 

                            else:
                                print("Invalid option.")
                        else:
                            print("Invalid employee number.")
                            
                    except ValueError:
                        print("Invalid input. Please enter numbers.")

                case 5: 
                    exit_confirm = input("Are you sure? (y/n) ").lower()
                    if exit_confirm == 'y':
                        break
                
                case _:
                    print("Invalid option")

        except ValueError:
            print("Invalid input. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")


# Garante que a função main() só será executada quando o script for rodado diretamente
if __name__ == "__main__":
    main()