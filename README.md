# Human Resources Management System

Este projeto é um sistema de gerenciamento de recursos humanos (RH) desenvolvido em Python, com foco em princípios de orientação a objetos e na aplicação de padrões de projeto para criar um código robusto, organizado e de fácil manutenção.

## Funcionalidades Implementadas

-   **Cadastro e Gerenciamento de Funcionários:** Adicione, edite, visualize e remova funcionários. Suporte a diferentes tipos: Funcionário, Gerente e Estagiário.
-   **Gestão de Benefícios:** Adicione, remova e visualize benefícios individuais de cada funcionário.
-   **Controle de Frequência:** Registre horários de entrada e saída, visualize registros e calcule horas trabalhadas.
-   **Avaliação de Performance:** Adicione, remova e visualize avaliações de desempenho dos funcionários.
-   **Gestão de Treinamentos:** Agende, remova e visualize sessões de treinamento para cada funcionário.
-   **Solicitações de Afastamento:** Gerencie pedidos de afastamento (férias, licenças, etc).
-   **Cálculo de Pagamentos:** Calcule o pagamento de cada funcionário com base em diferentes estratégias (ex: por hora, mensal).
-   **Relatórios de Compliance:** Registre, remova e visualize violações de compliance e gere relatórios.
-   **Notificações Automáticas:** O sistema notifica módulos interessados (Observers) sobre alterações em dados críticos (ex: salário).

## Refatoração e Padrões de Projeto Aplicados

O código foi submetido a um processo de refatoração para melhorar sua estrutura, aplicando os seguintes padrões de projeto:

1.  **Estruturação Inicial:** O código, que antes residia em um único arquivo, foi modularizado em `models.py`, `services.py`, `main.py`, etc., seguindo o princípio da **Separação de Responsabilidades**.

### Padrões Criacionais

2.  **Factory Method (Simple Factory):**
    -   **Problema:** A criação de diferentes tipos de funcionários estava acoplada diretamente à lógica principal (`main.py`).
    -   **Solução:** A `EmployeeFactory` foi criada para centralizar e encapsular a lógica de instanciação, desacoplando o código cliente da criação de objetos.

3.  **Builder:**
    -   **Problema:** Os construtores das classes de funcionário exigiam uma longa e inflexível lista de parâmetros.
    -   **Solução:** O `EmployeeBuilder` foi implementado para permitir a construção de objetos complexos passo a passo, tornando o código mais legível e escalável.

4.  **Singleton:**
    -   **Problema:** O estado da aplicação (as listas de funcionários) era gerenciado de forma descentralizada.
    -   **Solução:** A classe `HRSystem` foi criada como um Singleton para garantir uma única instância que gerencia todo o estado do sistema, funcionando como um ponto de acesso global e seguro.

### Padrões Comportamentais

5.  **Strategy:**
    -   **Problema:** A lógica de cálculo de pagamento era fixa (apenas por hora), dificultando a adição de novas formas de cálculo (ex: salário mensal).
    -   **Solução:** Foi definida uma família de algoritmos de pagamento (`HourlyPaymentStrategy`, `MonthlyPaymentStrategy`). A classe `PaymentContext` agora utiliza um desses objetos de estratégia para realizar o cálculo, permitindo que o método de pagamento seja alterado dinamicamente.

6.  **Observer:**
    -   **Problema:** Não havia um mecanismo para que outras partes do sistema fossem notificadas sobre mudanças importantes nos dados de um funcionário (ex: alteração de salário).
    -   **Solução:** A classe `Employee` foi transformada em um "Subject" (Observável). Agora, objetos "Observers" (como o `PayrollNotifier`) podem se registrar para serem notificados automaticamente sempre que o estado do funcionário muda, garantindo baixo acoplamento.

7.  **Template Method:**
    -   **Problema:** A geração de diferentes tipos de relatórios (Frequência, Compliance) não seguia uma estrutura padronizada, levando a código duplicado ou inconsistente.
    -   **Solução:** A classe abstrata `Report` implementa um `generate_report` que funciona como um "template". Este método define a estrutura do relatório (cabeçalho, corpo, rodapé) e chama métodos abstratos que as subclasses (`Attendance`, `Compliance`) devem implementar para fornecer o conteúdo específico de cada seção.

8.  **Command:**
    -   **Problema:** A lógica do menu principal (`main.py`) estava fortemente acoplada aos métodos da classe `Employee`. Cada nova ação exigia uma nova lógica condicional diretamente no menu.
    -   **Solução:** Ações como "Adicionar Treinamento" e "Adicionar Avaliação" foram encapsuladas em objetos de comando (`AddTrainingCommand`, `AddPerformanceEvaluationCommand`). O menu agora cria e executa esses objetos, desacoplando o "invocador" da ação do "executor" da ação, o que torna o sistema mais flexível e extensível.

### Padrões Estruturais

9.  **Composite:**
    -   **Problema:** Precisávamos representar a hierarquia organizacional (empresa -> departamentos -> funcionários) e tratar todos os níveis da hierarquia de forma uniforme.
    -   **Solução:** Foi criada a interface `OrganizationalComponent` (`models.py`) implementada tanto pela classe "folha" (`Employee`) quanto pela classe "container" (`Department`). Isso nos permite chamar o método `display_hierarchy()` no objeto raiz da empresa, e o comando se propaga recursivamente por toda a árvore, exibindo a estrutura completa.

10.  **Decorator:**
    -   **Problema:** A lógica de cálculo de pagamento (Padrão Strategy) precisava ser estendida para incluir adições (como bônus) e deduções (como impostos) sem criar uma subclasse para cada combinação possível.
    -   **Solução:** O `PaymentStrategy` (`services.py`) foi usado como a interface do componente. As classes `ManagerBonusDecorator` e `TaxDeductionDecorator` foram criadas como "embrulhadores" que também seguem a interface `PaymentStrategy`. Isso permite "empilhar" responsabilidades dinamicamente (ex: `TaxDeduction(ManagerBonus(HourlyPayment))`) antes de passar o objeto final para o `PaymentContext`.

11.  **Facade:**
    -   **Problema:** O código cliente (`main.py`) precisava conhecer e interagir com múltiplos subsistemas (Factory, Singleton, Strategy, Decorator) para realizar tarefas comuns, como contratar um funcionário ou calcular um pagamento.
    -   **Solução:** Foi criada a classe `HRFacade` (`facade.py`) que fornece uma interface única e simplificada. O `main.py` agora só conversa com a fachada, chamando métodos como `hire_employee()` ou `calculate_payment()`. A fachada, por sua vez, coordena internamente todos os subsistemas complexos necessários para executar a tarefa.

## Tratamento de Exceções

O sistema implementa um tratamento robusto e específico de exceções em todas as camadas do código, utilizando exceções customizadas organizadas hierarquicamente:

### Estrutura de Exceções

-   **Hierarquia de Exceções:** Todas as exceções do sistema herdam de `HRSystemException`, permitindo tratamento genérico quando necessário e específico quando apropriado. Exceções específicas são organizadas por domínio (dados de funcionário, frequência, pagamento, etc.).

-   **Exceções por Domínio:**
    -   **Dados de Funcionário:** `InvalidNameException`, `InvalidAgeException`, `InvalidEmailException`, `InvalidDepartmentException`, `InvalidSalaryException`
    -   **Operações do Sistema:** `InvalidEmployeeIndexException`, `InvalidEmployeeTypeException`, `ListSynchronizationException`
    -   **Frequência:** `ClockInWithoutClockOutException`, `ClockOutWithoutClockInException`, `NoAttendanceRecordsException`
    -   **Pagamento:** `InvalidPaymentCalculationException`, `NegativePaymentException`
    -   **Outras:** `InvalidPerformanceLevelException`, `BenefitAlreadyExistsException`, `BenefitNotFoundException`

### Características da Implementação

1.  **Validação em Múltiplas Camadas:** O sistema valida dados em diferentes pontos:
    -   **Camada de Interface (`main.py`):** Validação de inputs do usuário (tipos, ranges, valores vazios)
    -   **Camada de Facade (`facade.py`):** Validação de parâmetros antes de delegar para subsistemas
    -   **Camada de Modelo (`models.py`):** Validação de propriedades através de setters
    -   **Camada de Serviço (`services.py`):** Validação de regras de negócio e cálculos

2.  **Mensagens de Erro Específicas:** Cada exceção fornece mensagens detalhadas que incluem:
    -   O tipo de erro ocorrido
    -   O valor recebido (quando aplicável)
    -   O valor esperado ou range válido
    -   Contexto adicional quando relevante

3.  **Integridade de Dados:** 
    -   **Rollback:** Operações complexas (como adicionar funcionário) implementam rollback em caso de falha parcial
    -   **Sincronização:** Verificação de consistência entre listas relacionadas (funcionários, frequência, compliance)
    -   **Validação de Índices:** Verificação rigorosa de índices antes de acessar listas, evitando erros de runtime

4.  **Tratamento de Casos Especiais:**
    -   Validação de sequência de operações (ex: clock in/out)
    -   Verificação de valores negativos em cálculos financeiros
    -   Validação de tipos antes de operações críticas
    -   Tratamento de objetos None e listas vazias

## Justificativa das Funcionalidades Ausentes

-   **Recruitment and Onboarding:** Não implementado por ser um subsistema complexo com um escopo de dados e regras de negócio distinto da gestão de funcionários internos.
-   **Employee Self-Service Portal:** Não implementado por exigir uma arquitetura de software diferente (GUI ou Web) com requisitos de segurança e autenticação fora do escopo deste projeto de terminal.

## Como Executar

1.  **Pré-requisitos:**
    -   Python 3.x instalado.

2.  **Execução:**
    -   No terminal, navegue até a pasta do projeto e execute o arquivo principal: `python main.py`.
    -   Siga as instruções do menu interativo.

---

*Desenvolvido por David Kelve Oliveira Barbosa*

*Refatorado por José Lucas Oliveira Quintela*
