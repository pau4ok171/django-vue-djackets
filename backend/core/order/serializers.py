from rest_framework.serializers import ModelSerializer

from product.serializers import ProductSerializer

from .models import Order, OrderItem


class OrderItemSerializer(ModelSerializer):

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'price',
            'quantity',
        )


class CustomerOrderItemSerializer(ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'price',
            'quantity',
        )


class OrderSerializer(ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'zipcode',
            'place',
            'stripe_token',
            'items',
        )

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order


class CustomerOrderSerializer(ModelSerializer):
    items = CustomerOrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'address',
            'zipcode',
            'place',
            'stripe_token',
            'items',
            'paid_amount',
        )

