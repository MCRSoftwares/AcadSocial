# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v002a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das mensagens de erro relacionados à aplicação de contas (cadastro/login).
"""

# Erros relacionados ao forms.py: Cadastro

erro_senhas_diferentes = ('As senhas estão diferentes!', 'cadastro_e01')

erro_email_ja_existe = ('Esse e-mail já está cadastrado!', 'cadastro_e02')

erro_data_incorreta = ('Essa data não existe!', 'cadastro_e03')