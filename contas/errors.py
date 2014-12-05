# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das mensagens de erro relacionados à aplicação de contas (cadastro/login).
"""

# Erros relacionados ao forms.py

erro_cadastro = {
    'senhas_diferentes': 'As senhas estão diferentes!',
    'email_ja_existente': 'Esse e-mail já está cadastrado!',
    'data_incorreta': 'Essa data não existe!',
}

erro_login = {
    'login_invalido': 'E-mail ou senha incorretos!',
    'email_inativo': 'Esse e-mail não está ativado!',
}