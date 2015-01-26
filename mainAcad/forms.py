# -*- encoding: utf-8 -*-

"""
Equipe MCRSoftwares - AcadSocial

Versão do Código: 01v003a

Responsável: Victor Ferraz
Auxiliar: -

Requisito(s): -
Caso(s) de Uso: -

Descrição:
    Definição dos forms relacionadas à aplicação principal.
"""

from django import forms
from contas.models import UsuarioModel
from mainAcad.models import ImagemModel
from mainAcad.constants import MAX_IMAGE_SIZE
from mainAcad.errors import erro_imagem


class UsuarioSearchForm(forms.ModelForm):

    pesquisa_attrs = {'placeholder': 'Pesquisar...', 'class': 'form-control'}

    q = forms.CharField(max_length=256, widget=forms.TextInput(attrs=pesquisa_attrs))

    class Meta:
        model = UsuarioModel
        fields = ()


class ImagemUploadForm(forms.ModelForm):

    imagem_attrs = {'accept': 'image/x-png, image/gif, image/jpeg, image/jpg',
                    'id': 'imageID', 'style': 'display:none;', 'name': 'file'}

    imagem = forms.ImageField(widget=forms.FileInput(attrs=imagem_attrs), required=False)

    def clean(self):

        if 'imagem' in self.files:

            imagem = self.files['imagem']

            # Checa se a foto possui o tamanho máximo definido (4MB).

            if imagem.size > MAX_IMAGE_SIZE:
                raise forms.ValidationError(erro_imagem['limite_tamanho'], code='limite_tamanho')

        return self.cleaned_data

    class Meta:
        model = ImagemModel
        fields = ('imagem',)


class ContatoForm(forms.ModelForm):

    nome_attrs = {
        'class': 'form-control',
    }

    email_attrs = {
        'class': 'form-control',
    }

    assunto_attrs = {
        'class': 'form-control',
    }

    conteudo_attrs = {
        'class': 'form-control',
        'maxlength': '1024',
        'rows': '3',
    }

    nome = forms.CharField(max_length=256, widget=forms.TextInput(attrs=nome_attrs))
    email = forms.CharField(max_length=128, widget=forms.EmailInput(attrs=email_attrs))
    assunto = forms.CharField(max_length=256, widget=forms.TextInput(attrs=assunto_attrs))
    conteudo = forms.CharField(max_length=1024, widget=forms.Textarea(attrs=conteudo_attrs))

    class Meta:
        model = UsuarioModel
        fields = ('nome', 'email', 'assunto', 'conteudo',)