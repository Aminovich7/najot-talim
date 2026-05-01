from rest_framework import serializers
from serializer_crud.models import Watch
from decimal import Decimal



class WatchCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Watch
        fields = "__all__"


    def validate(self, attrs):
        price = attrs.get('price')
        if price:
            if price<=0:
                raise serializers.ValidationError('Narx notogri kirildi!')

        return attrs


    def validate_brand(self, value):
        if value.isdigit():
            raise serializers.ValidationError('Raqamdan iborat bolmasin!')
        return value

    def create(self, validated_data):
        soat = super().create(validated_data)
        # price = validated_data.get('price')
        # discount = validated_data.get('discount')
        #
        # if discount:
        #     total_price = price * Decimal(f"{(1 - discount / 100)}")
        #     soat.total_price = total_price
        #     soat.save()

        return soat

    def to_representation(self, instance):
        data = super(WatchCreateSerializer, self).to_representation(instance)
        data.update({
            'status': 'success',
            'message': 'Product created successfully!'
        })
        return data

class WatchUpdateSerializer(WatchCreateSerializer):
    def update(self, instance, validated_data):
        brand = validated_data.get('brand')
        country = validated_data.get('country')
        price = validated_data.get('price')
        discount = validated_data.get('discount')

        if brand:
            instance.brand = brand
        if country:
            instance.country = country
        if price:
            instance.price = price
        if discount:
            instance.discount = discount


        instance.save()
        return instance

    def to_representation(self, instance):
        data = super(WatchCreateSerializer, self).to_representation(instance)
        data.update({
            'status': 'success',
            'message': 'Product updated successfully!'
        })
        return data


class WatchListSerializer(WatchCreateSerializer):
    def to_representation(self, instance):
        data = super(WatchCreateSerializer, self).to_representation(instance)
        return data
