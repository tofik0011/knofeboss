from rest_framework import serializers

from apps.products.models import Product


class ProductSerializer(serializers.Serializer):
    # name = serializers.CharField(max_length=255)
    price = serializers.DecimalField(decimal_places=2, max_digits=9)

    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # instance.name = validated_data.get('name')
        instance.price = validated_data.get('price')
        instance.save()
        return instance


class ProductSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('price',)
