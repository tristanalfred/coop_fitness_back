from rest_framework import serializers
from sante.models import Exercice, Seance, Serie, Programme, ProgrammeSportIndividuel


class ExerciceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercice
        fields = '__all__'


class ExerciceMinimumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercice
        fields = ['id', 'nom', 'conseils']


class SerieSerializer(serializers.HyperlinkedModelSerializer):
    # seances = ExerciceMinimumSerializer(read_only=True)
    # seancee = serializers.RelatedField(source='seance', read_only=True)
    seancee = serializers.StringRelatedField(source='seance', read_only=True)

    class Meta:
        model = Serie
        # fields = '__all__'
        # fields = ('repetition', 'seances',)
        fields = ('id', 'repetition', 'seancee')


class SeanceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seance
        fields = '__all__'


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    seance = SeanceSerializer(read_only=True, many=True)

    class Meta:
        model = Programme
        # fields = '__all__'
        fields = ['id', 'nom', 'description', 'seance']


class ProgrammeSportIndividuelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgrammeSportIndividuel
        fields = '__all__'
