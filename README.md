# Human Resources Management System

Este projeto é um sistema de gerenciamento de recursos humanos (RH) desenvolvido em Python, com foco em princípios de orientação a objetos e na aplicação de padrões de projeto para criar um código robusto, organizado e de fácil manutenção.

## Funcionalidades Implementadas

-   **Cadastro e Gerenciamento de Funcionários:** Adicione, edite, visualize e remova funcionários. Suporte a diferentes tipos: Funcionário, Gerente e Estagiário.
-   **Gestão de Benefícios:** Adicione, remova e visualize benefícios individuais de cada funcionário.
-   **Controle de Frequência:** Registre horários de entrada e saída, visualize registros e calcule horas trabalhadas.
-   **Avaliação de Performance:** Adicione, remova e visualize avaliações de desempenho dos funcionários.
-   **Gestão de Treinamentos:** Agende, remova e visualize sessões de treinamento para cada funcionário.
-   **Solicitações de Afastamento:** Gerencie pedidos de afastamento (férias, licenças, etc).
-   **Cálculo de Pagamentos:** Calcule o pagamento de cada funcionário com base nas horas trabalhadas.
-   **Relatórios de Compliance:** Registre, remova e visualize violações de compliance e gere relatórios.

## Refatoração e Padrões de Projeto

O código original foi submetido a um processo de refatoração para melhorar sua estrutura e manutenibilidade, aplicando os seguintes padrões de projeto criacionais:

1.  **Estruturação Inicial:** O código, que antes residia em um único arquivo, foi modularizado em diferentes arquivos (`models.py`, `services.py`, `main.py`, etc.), seguindo o princípio da **Separação de Responsabilidades**.

2.  **Factory Method (Simple Factory):**
    -   **Problema:** A criação de diferentes tipos de funcionários (`Employee`, `Manager`, `Intern`) estava acoplada diretamente à lógica da interface principal (`main.py`) através de um bloco `if/elif/else`.
    -   **Solução:** Foi criada a `EmployeeFactory`, que centraliza e encapsula a lógica de instanciação. Isso desacoplou o código cliente da criação de objetos, tornando o sistema mais flexível a novos tipos de funcionários.

3.  **Builder:**
    -   **Problema:** Os construtores das classes de funcionário exigiam uma longa e inflexível lista de parâmetros, dificultando a leitura e a criação dos objetos.
    -   **Solução:** Foi implementado o `EmployeeBuilder`, que permite a construção de um objeto complexo passo a passo. Isso tornou a criação de funcionários mais legível, flexível e escalável para futuros atributos.

4.  **Singleton:**
    -   **Problema:** O estado da aplicação (as listas de funcionários, presenças, etc.) era gerenciado de forma descentralizada, dificultando o controle e o acesso consistente aos dados.
    -   **Solução:** A classe `HRSystem` foi criada como um Singleton, garantindo uma única instância para gerenciar todo o estado do sistema. Ela funciona como um ponto de acesso global e seguro aos dados, centralizando a lógica de negócio.

## Justificativa das Funcionalidades Ausentes

Conforme a análise de requisitos, duas funcionalidades de alto nível não foram implementadas. A justificativa se baseia na complexidade e no escopo definido para este projeto:

-   **Recruitment and Onboarding (Recrutamento e Integração):**
    -   **Justificativa:** Um módulo de recrutamento é, em essência, um subsistema completo. Ele lida com entidades externas (candidatos), múltiplas etapas (triagem, entrevistas, oferta) e requer um modelo de dados e regras de negócio distintos do gerenciamento de funcionários internos. A implementação demandaria um escopo significativamente maior, fugindo do foco central do projeto, que é a gestão de funcionários já contratados.

-   **Employee Self-Service Portal (Portal de Autoatendimento):**
    -   **Justificativa:** A implementação de um "portal" pressupõe uma arquitetura de software diferente da adotada (interface de linha de comando administrativa). Exigiria a criação de uma interface gráfica (GUI) ou web, com sistemas de autenticação de usuário, gerenciamento de sessão e controle de permissões por nível de acesso. Tais requisitos de arquitetura e segurança extrapolam o escopo de um projeto focado na aplicação de padrões de OO em um ambiente de terminal.

## Como Executar

1.  **Pré-requisitos:**
    -   Python 3.x instalado.

2.  **Execução:**
    -   No terminal, navegue até a pasta do projeto e execute o arquivo principal (ex: `main.py`).
    -   Siga as instruções do menu interativo.

---

*Desenvolvido por David Kelve Oliveira Barbosa*

*Refatorado por José Lucas Oliveira Quintela*