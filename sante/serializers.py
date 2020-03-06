from rest_framework import serializers
from sante.models import Exercice, Seance, SeanceFav, SeanceProgramme, Serie, Programme, ProgrammeSportIndividuel
from connection_front.models import Utilisateur
from connection_front.serializers import UtilisateurSerializer


class ExerciceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercice
        fields = '__all__'


class ExerciceMinimumSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercice
        fields = ['id', 'nom', 'conseils']


class ExerciceNomSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Exercice
        fields = ['nom']


class ExercicePlusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercice
        fields = ['id', 'nom', 'conseils']


class SerieSerializer(serializers.ModelSerializer):
    # exercice = ExerciceSerializer()

    class Meta:
        model = Serie
        # fields = ('id', 'repetition', 'exercice')
        fields = '__all__'


class SerieSeanceSerializer(serializers.ModelSerializer):
    # exercice = ExerciceSerializer()

    class Meta:
        model = Serie
        fields = ('repetition', 'exercice')
        # fields = '__all__'


class SerieReadSerializer(serializers.HyperlinkedModelSerializer):
    exercice = serializers.StringRelatedField()

    class Meta:
        model = Serie
        fields = ('repetition', 'exercice')


class SerieMinimumSerializer(serializers.HyperlinkedModelSerializer):
    exercice = serializers.StringRelatedField()

    class Meta:
        model = Serie
        fields = ('repetition', 'exercice')


class SeanceTestSerializer(serializers.ModelSerializer):
    series = SerieSeanceSerializer(many=True)

    class Meta:
        model = Seance
        fields = ('date', 'num_jour', 'series')

    def create(self, validated_data):
        print('CREATE')
        series_data = validated_data.pop('series')
        seance = Seance.objects.create(**validated_data)
        for serie_data in series_data:
            Serie.objects.create(seance=seance, **serie_data)
        return seance


class SeanceSerializer(serializers.ModelSerializer):
    # serie = serializers.PrimaryKeyRelatedField(many=True, queryset=Serie.objects)  # En cours
    serie = SerieSerializer(many=True)  # En cours

    class Meta:
        model = Seance
        # fields = '__all__'
        fields = ('id', 'date', 'num_jour', 'serie')
        depth = 2

    def create(self, validated_data):
        print('on crée')


class SeanceReadSerializer(serializers.ModelSerializer):
    serie = SerieSerializer(many=True)

    class Meta:
        model = Seance
        fields = ('id', 'date', 'num_jour', 'serie')


# class SeanceSerializer(serializers.ModelSerializer):
#     series = SerieSerializer(many=True)
#
#     class Meta:
#         model = Seance
#         # fields = '__all__'
#         fields = ('id', 'num_jour', 'date', 'series')
#         # depth = 2
#
#     def create(self, validated_data):
#         print('- CREATE -')
#         series_data = validated_data.pop('tracks')
#         seance = Seance.objects.create(**validated_data)
#         for serie_data in series_data:
#             Serie.objects.create(seance=seance, **serie_data)
#         return seance


# class SeanceReadSerializer(SeanceSerializer):
#     serie = SerieSerializer(many=True, read_only=True)


class SeanceMinimumSerializer(serializers.HyperlinkedModelSerializer):
    serie = SerieMinimumSerializer(many=True)

    class Meta:
        model = Seance
        fields = ('url', 'num_jour', 'date', 'serie')


class ProgrammeSportIndividuelSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ProgrammeSportIndividuel
        fields = '__all__'


class SeriePlusSerializer(serializers.ModelSerializer):  # TODO : on garde
    exercice = serializers.PrimaryKeyRelatedField(queryset=Exercice.objects)

    class Meta:
        model = Serie
        fields = ('repetition', 'exercice')


class SeancePlusSerializer(serializers.ModelSerializer):  # TODO : on garde
    serie = SeriePlusSerializer(many=True)

    class Meta:
        model = Seance
        fields = ('action', 'date', 'num_jour', 'serie')

    action = serializers.SerializerMethodField(method_name="get_data_for_action")

    def create(self, validated_data):
        series_data = validated_data.pop('serie')
        seance = Seance.objects.create(**validated_data)
        for serie_data in series_data:
            # Une série similaire existe déjà
            if Serie.objects.filter(repetition=list(serie_data.items())[0][1])\
                    .filter(exercice=list(serie_data.items())[1][1])\
                    .count() > 0:
                serie = Serie.objects.filter(repetition=list(serie_data.items())[0][1])\
                    .filter(exercice=list(serie_data.items())[1][1]).first()
            # Nouvelle série
            else:
                serie = Serie.objects.create(**serie_data)

            seance.serie.add(serie)
        return seance

    def get_data_for_action(self, obj):
        utilisateur = Utilisateur.objects.get(id=self.context['request'].user.id)
        SeanceFav.objects.create(seance=obj, utilisateur=utilisateur)


class SeanceFavSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeanceFav
        fields = '__all__'


class ProgrammeSerializer(serializers.HyperlinkedModelSerializer):
    seance = SeanceMinimumSerializer(read_only=True, many=True)
    createur = serializers.PrimaryKeyRelatedField(queryset=Utilisateur.objects)

    class Meta:
        model = Programme
        fields = ['id', 'nom', 'description', 'createur', 'seance']


class SeanceCreateProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeanceProgramme
        fields = '__all__'


class SeanceProgrammeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SeanceProgramme
        fields = '__all__'

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
