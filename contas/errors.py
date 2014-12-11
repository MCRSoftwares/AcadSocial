# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v005a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): RF001, RF002
Caso(s) de Uso: DV001, DV002

Descrição:
    Definição das mensagens de erro relacionados à aplicação de contas (cadastro/login).
"""

from contas.constants import MAX_IMAGE_SIZE

# Erros relacionados ao forms.py

erro_cadastro = {
    'senhas_diferentes': 'As senhas estão diferentes!',
    'email_ja_existente': 'Esse e-mail já está cadastrado!',
    'data_incorreta': 'Essa data não existe!',
    'email_invalido': 'Esse e-mail não é válido!',
    'nome_incompleto': 'O campo \'nome\' deve conter pelo menos dois caracteres!',
    'sobrenome_incompleto': 'O campo \'sobrenome\' deve conter pelo menos dois caracteres!',
    'nome_invalido': 'O campo \'nome\' não pode conter valores numéricos!',
    'sobrenome_invalido': 'O campo \'sobrenome\' não pode conter valores numéricos!',
    'senha_invalida': 'A senha deve ter pelo menos 6 caracteres, contendo pelo menos 1 letra e 1 número e sem espaços.',
    'foto_limite_tamanho': 'A imagem deve ter no máximo %s.%sMB!' % (str(MAX_IMAGE_SIZE)[0], str(MAX_IMAGE_SIZE)[1]),
}

erro_login = {
    'login_invalido': 'E-mail ou senha incorretos!',
    'email_inativo': 'Esse e-mail não está ativado!',
}

erro_enviar_token = {
    'email_invalido': 'Esse e-mail não está cadastrado!',
    'senhas_diferentes': 'As senhas estão diferentes!',
    'senha_invalida': 'A senha deve ter pelo menos 6 caracteres, contendo pelo menos 1 letra e 1 número e sem espaços.',
}