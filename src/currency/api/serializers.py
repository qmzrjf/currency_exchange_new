from currency.models import Rate
from rest_framework import serializers


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ('id', 'created', 'currency', 'buy', 'sale', 'source')

        extra_kwargs = {
            'currency': {'write_only': True},
            'source': {'write_only': True}
        }