# Pentago com Q-Learning

Este projeto implementa o algoritmo Q-learning para treinar um agente capaz de jogar o jogo Pentago de forma eficaz contra um oponente. O Pentago é um jogo de tabuleiro de estratégia abstrata para dois jogadores, inventado por Tomas Flodén. O objetivo do jogo é formar um padrão de cinco peças de sua cor (branco ou preto) em linha reta, em qualquer direção (horizontal, vertical ou diagonal), em qualquer um dos quatro blocos do tabuleiro.

## Sobre o Algoritmo Q-learning

O Q-learning é um algoritmo de aprendizado por reforço que permite que um agente aprenda a tomar decisões ótimas em um ambiente desconhecido, maximizando a recompensa cumulativa ao longo do tempo. O agente aprende uma função de valor de ação, chamada de função Q, que atribui um valor a cada par estado-ação, representando a utilidade esperada de escolher a ação em um determinado estado. O algoritmo atualiza iterativamente os valores Q com base em recompensas recebidas e estimativas futuras de recompensas.

## Como Usar Este Projeto

### Agente Q-Learning

1. Por questões de limitações do github, deve ser baixado o agente treinado para a sua máquina no link: [agent_data.pkl](https://drive.google.com/drive/folders/1LBSt7D-3sxEtloBZD2VZmnQxPwdOf7hX?usp=sharing)
2. Após baixado, ele deve ser inserido na raiz do repositório para que possa jogar e treiná-la. 

### Dependências

- Python 3.x
- Bibliotecas Python: `numpy`, `pickle`, `os`, `random`

### Execução

1. Clone este repositório em sua máquina local.
2. Certifique-se de ter todas as dependências instaladas.
3. Execute o arquivo `main.py` para jogar contra o agente ou o arquivo `train.py` para treinar o agente contra ele mesmo:

```bash
python main.py
python train.py
```

### Customização

- Você pode ajustar os hiperparâmetros de aprendizado e outras configurações no arquivo `agent.py`.
- Para modificar o comportamento do oponente Minimax, você pode ajustar a implementação do algoritmo no arquivo `minimax.py`.

## Resultados Esperados

Após o treinamento, o agente Q-learning deve ser capaz de jogar o Pentago contra um oponente, demonstrando estratégias aprendidas ao longo do tempo. Os resultados do treinamento, incluindo o número de vitórias do agente, derrotas do oponente e empates, serão exibidos no terminal.

## Integrantes do grupo

- Carolina Gimenez
- Eduarda Medeiros