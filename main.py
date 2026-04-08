from collections import namedtuple

pessoa = namedtuple('Pessoa', 'nome sobrenome telefone ddd')

dados = [
  pessoa('Eduardo', 'Mendes', {'residencial': '1111-111', 'móvel': '999-999-999'}, 19),
  pessoa('Gabriel', 'Dornas', {'residencial': '2222-2222', 'móvel': '888-888-888'}, 20),
]

eduardo = dados[0]
print(eduardo.nome)
print(eduardo.sobrenome)
print(eduardo.telefone)
print(eduardo.ddd)
