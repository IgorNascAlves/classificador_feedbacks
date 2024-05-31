# Journal

## 27/05/2024

- Acabei criando a base do projeto e a primeira feature no mesmo commit. Não é uma boa prática, mas como é um projeto pequeno, acho que não terá problemas.

## 28/05/2024

- Como testar respostas da LLM's se o conteudo é incerto? (FAILED tests/test_feedback.py::test_analyze_feedback_feature_identification_negative - AssertionError: assert 'VISUALIZAR_AULAS' == 'ASSISTIR_AULAS')
- Terminei a primera feature colocando o recurso de identificar funcionalidades pedidas pelo usuário.
- O teste não passou por falta de um campo, aparamente nem isso da para confiar na LLMs preciso adcionar validação antes de responder
- Os dados estao sendo salvos em um banco de dados MySQL, porquem os dados de teste tambem, tive que buscar uma configuração nova para resolver isso
- Preciso tratar IDs iguais
- Preciso garantir os campos do json idependente do que a LLM respondeu

## 29/05/2024

- Mandar as categorias existentes no prompt para ele escolher entre elas ou pedir uma nova.
Estou tendo problemas com as features ele ta criando umas bem ruins preciso melhorar o prompt e incluir mais exemplos (que vou armazenando com o tempo)
- Ele fez uma categoria chamada None, não sei como é isso, preciso investigar

## 30/05/2024

- Validar Imports realizados apos a inicialização das extensões Flask para evitar erros de importação circular no main.py

## 31/05/2024 - Deadline (12:00)

Tarefas pendentes:

Tarefas principais:
- [x] Validar se ID já existe
- [x] Melhorar a documentação
- [x] Ajustes no tutorial de configuração
- [ ] Bug de email agendado (fora do contexto)
- [ ] Bug que aparece funcionalidade invalida
- [ ] Adicionar validação antes de responder (Tanto de entrada quanto de saída e tambem se os campos estão dentro do previsto como POSITIVO, NEGATIVO, INCONCLUSIVO)
- [x] Enviar projeto

Tarefas opcionais:
- [x] Utilizar LLM para montar texto do email
- [ ] Classificador de SPAM antes de reconhecer a funcionalidade e sentimentos
- [ ] Melhorar o prompt de identificação de funcionalidades
- [ ] Adicionar sweeger
- [ ] Publicar no Pythonanywhere
- [ ] Criar tarefas no Trello
- [ ] Buscador por ID do feedback na pagina de report
