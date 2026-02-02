import random

class TriviaGameLogic:
    def __init__(self, perguntas):
        self.perguntas = perguntas
        random.shuffle(self.perguntas)
        self.index = 0
        self.pontuacao = 0

    def proxima_pergunta(self):
        if self.index >= len(self.perguntas):
            return None
        p = self.perguntas[self.index]

        # Embaralhar opções
        opcoes = p['opcoes'][:]
        random.shuffle(opcoes)
        p['opcoes_embaralhadas'] = opcoes

        self.index += 1
        return p

    def verificar_resposta(self, pergunta, escolha):
        return escolha == pergunta['correta']
