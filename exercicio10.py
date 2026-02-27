# Bingo - Desafio Gabriel

# 75 números, de 1 a 75.
# Números sorteados, sem repetição.
# O jogo termina quando todos os números forem sorteados (75 rodadas).
# O jogo somente printará os números sorteados, um por rodada, e a rodada atual, até a última rodada.

numeros = list(range(1, 76))

for rodada in range(75):
    import random
    numero_sorteado = random.choice(numeros)
    numeros.remove(numero_sorteado)
    print(f"Rodada {rodada}: Número sorteado - {numero_sorteado}")

# Vamos criar um stremlit disso?
