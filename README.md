Programa: acl-converter.py

1. Introdução: 
acl-converter.py é um front-end para a classe em Python fw_rules (fw_rules.py), que por sua vez implementa
métodos para converter regras de filtragem de pacotes usando sintaxes suportados por diversos firewalls.

Entre os formatos implementados, temos:
- csv: Lista separada por virgula, para documentação / visualização de regras em planilhas.
- acl: Sintaxe de Access Control Lists usada pela Brocade/Extreme/Ruckus
- ipfw: Regras na sintaxe do IPFW (FreeBSD)
- pf: Formato (XML) importado/exportado pelo pfSense 

2. Descrição:
A classe fw_rule implementa uma série de métodos para conversão (de/para) entre os formatos acima e a representação usada internamente para as regras, através de um dicionário Python. A conversão de um formato arbitrário A para outro formato B pode ser implementada da seguinte forma:

- Definindo-se, se não houver, um método de tradução (parser) do formato A para o dicionário, com o nome from_A (o "from_" inicial é mandatório);
- Idem, para conversão do dicionário para o formato B, com o nome to_B
- Criando-se um link com o nome A2B para o executável acl_converter.py.

Por exemplo, para criar um script que converta ACLs no formato Brocade para a sintaxe do iptables (Linux):
- Definir um parser from_acl, que interpreta a sintaxe das ACLs e gere o dicionário.
- Outro parser, to_iptables, que gera as regras no formato entendido pelo IPTABLES a parte da sintaxe genérica do dicionário.
- Criar um link acl2iptables.

3. Formatos:

O dicionário interno reconhece os seguintes campos:

'id': 1, # Id da regra, usado para preservar a ordenação
'action': '', # permit | deny 
'proto': '',  # Protocolo: ip | tcp | udp | ...
'src': # Origem: 
    'addr': '', # Endereço(s) de origem. String com um CSV contendo um lista de IPs ou CIDRs. O valor 'any' descreve qualquer origem.
    'port': ('null', 'null')}, # Portas de origem TCP/UDP, na formato de range (min, max). Uma porta única é indicada pelo
                                   # mesmo valor para min e max
'dst': # Destino 
{'addr': '', # Idem para endereços de destino.
        'port': ('null', 'null')}, # Idem para portas de destino.
'opts': [], # Vetor contendo opções dependentes do protocolo 
'drt': 'in', # Sentido do tráfego: in | out | both
'intf': '' # Interface ao qual se aplica a regra