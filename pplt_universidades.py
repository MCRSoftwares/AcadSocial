# -*- encoding: utf-8 -*-

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AcadSocial.settings')
django.setup()

from universidades.models import UniversidadeModel, CursoModel


def populate():

    # Universidades

    ufpe_recife = add_univ('Universidade Federal de Pernambuco', 'UFPE', 'Recife')
    ufpe_caruaru = add_univ('Universidade Federal de Pernambuco', 'UFPE', 'Caruaru')
    ufpe_vitoria = add_univ('Universidade Federal de Pernambuco', 'UFPE', u'Vitória')

    # Cursos

    add_curso(u'Ciências Biológicas - Licenciatura', ufpe_vitoria)
    add_curso(u'Educação Física - Bacharelado', ufpe_vitoria)
    add_curso(u'Educação Física - Licenciatura', ufpe_vitoria)
    add_curso(u'Enfermagem', ufpe_vitoria)
    add_curso(u'Nutrição - Bacharelado', ufpe_vitoria)
    add_curso(u'Saúde Coletiva', ufpe_vitoria)

    add_curso(u'Ciências Econômicas', ufpe_caruaru)
    add_curso(u'Design', ufpe_caruaru)
    add_curso(u'Engenharia Civil', ufpe_caruaru)
    add_curso(u'Engenharia de Produção', ufpe_caruaru)
    add_curso(u'Física - Licenciatura', ufpe_caruaru)
    add_curso(u'Matemática - Licenciatura', ufpe_caruaru)
    add_curso(u'Pedagogia', ufpe_caruaru)
    add_curso(u'Química', ufpe_caruaru)

    add_curso(u'Administração', ufpe_recife)
    add_curso(u'Arqueologia', ufpe_recife)
    add_curso(u'Arquitetura e Urbanismo', ufpe_recife)
    add_curso(u'Artes Visuais', ufpe_recife)
    add_curso(u'Biblioteconomia', ufpe_recife)
    add_curso(u'Biomedicina', ufpe_recife)
    add_curso(u'Ciência da Computação - Bacharelado', ufpe_recife)
    add_curso(u'Ciência Política', ufpe_recife)
    add_curso(u'Ciências Atuariais', ufpe_recife)
    add_curso(u'Ciências Biológicas - Bacharelado', ufpe_recife)
    add_curso(u'Ciências Biológicas - Ciências Ambientais', ufpe_recife)
    add_curso(u'Ciências Biológicas - Licenciatura', ufpe_recife)
    add_curso(u'Ciências Contábeis', ufpe_recife)
    add_curso(u'Ciências Econômicas', ufpe_recife)
    add_curso(u'Ciências Sociais - Bacharelado', ufpe_recife)
    add_curso(u'Ciências Sociais - Licenciatura', ufpe_recife)
    add_curso(u'Cinema e Audiovisuais', ufpe_recife)
    add_curso(u'Dança', ufpe_recife)
    add_curso(u'Design', ufpe_recife)
    add_curso(u'Direito', ufpe_recife)
    add_curso(u'Educação Física - Bacharelado', ufpe_recife)
    add_curso(u'Educação Física - Licenciatura', ufpe_recife)
    add_curso(u'Enfermagem', ufpe_recife)
    add_curso(u'Engenharia Biométrica', ufpe_recife)
    add_curso(u'Engenharia Cartográfica', ufpe_recife)
    add_curso(u'Engenharia Civil', ufpe_recife)
    add_curso(u'Engenharia da Computação', ufpe_recife)
    add_curso(u'Engenharia de Alimentos', ufpe_recife)
    add_curso(u'Engenharia de Controle e Automação', ufpe_recife)
    add_curso(u'Engenharia de Energia', ufpe_recife)
    add_curso(u'Engenharia de Materiais', ufpe_recife)
    add_curso(u'Engenharia de Minas', ufpe_recife)
    add_curso(u'Engenharia de Produção', ufpe_recife)
    add_curso(u'Engenharia Elétrica', ufpe_recife)
    add_curso(u'Engenharia Eletrônica', ufpe_recife)
    add_curso(u'Engenharia Mecânica', ufpe_recife)
    add_curso(u'Engenharia Naval', ufpe_recife)
    add_curso(u'Engenharia Química', ufpe_recife)
    add_curso(u'Estatística', ufpe_recife)
    add_curso(u'Expressão Gráfica', ufpe_recife)
    add_curso(u'Farmácia', ufpe_recife)
    add_curso(u'Filosofia - Bach/Licenciatura', ufpe_recife)
    add_curso(u'Física - Bacharelado', ufpe_recife)
    add_curso(u'Física - Licenciatura', ufpe_recife)
    add_curso(u'Fisioterapia', ufpe_recife)
    add_curso(u'Fonoaudiologia', ufpe_recife)
    add_curso(u'Geografia', ufpe_recife)
    add_curso(u'Turismo', ufpe_recife)
    add_curso(u'Terapia Ocupacional', ufpe_recife)
    add_curso(u'Teatro', ufpe_recife)
    add_curso(u'Sistemas de Informação', ufpe_recife)
    add_curso(u'Serviço Social', ufpe_recife)
    add_curso(u'Secretariado', ufpe_recife)
    add_curso(u'Rádio, Tv e Internet', ufpe_recife)
    add_curso(u'Química Industrial', ufpe_recife)
    add_curso(u'Química - Licenciatura', ufpe_recife)
    add_curso(u'Química - Bacharelado', ufpe_recife)
    add_curso(u'Publicidade e Propaganda', ufpe_recife)
    add_curso(u'Psicologia', ufpe_recife)
    add_curso(u'Pedagogia', ufpe_recife)
    add_curso(u'Odontologia', ufpe_recife)
    add_curso(u'Oceanografia', ufpe_recife)
    add_curso(u'Nutrição', ufpe_recife)
    add_curso(u'Música - Licenciatura', ufpe_recife)
    add_curso(u'Música - Instrumento', ufpe_recife)
    add_curso(u'Música - Canto', ufpe_recife)
    add_curso(u'Museologia', ufpe_recife)
    add_curso(u'Medicina', ufpe_recife)
    add_curso(u'Matemática - Licenciatura', ufpe_recife)
    add_curso(u'Matemática - Bacharelado', ufpe_recife)
    add_curso(u'Letras - Bacharelado/Licenciatura', ufpe_recife)
    add_curso(u'Jornalismo', ufpe_recife)
    add_curso(u'Hotelaria', ufpe_recife)
    add_curso(u'História', ufpe_recife)
    add_curso(u'Gestão da Informação', ufpe_recife)
    add_curso(u'Geologia', ufpe_recife)


def add_univ(nome, sigla, campus):

    print u'Adding Universidade: %s (%s) - Campus: %s' % (nome, sigla, campus)
    universidade = UniversidadeModel.objects.get_or_create(nome=nome, sigla=sigla, campus=campus)[0]
    print u'Done!'

    return universidade


def add_curso(nome, universidade):
    print u'Adding Curso: %s - %s' % (nome, universidade)
    curso = CursoModel.objects.get_or_create(nome=nome, universidade=universidade)[0]
    print u'Done!'

    return curso


if __name__ == '__main__':
    print u'Populating tables \"Universidades\" and \"Cursos\"'
    populate()