from rest_framework import serializers

from .models import JobOpening, Company


def is_valid_reward(value):
    if not isinstance(value, int):
        return serializers.ValidationError("reward have to be integer.")
        
    if value < 0 or value > 2147483647:
        return serializers.ValidationError("reward have to be 0~2147483647. value: {value}")


class CompanySerializer(serializers.ModelSerializer):
    class Meta():
        model=Company
        fields = '__all__'


class JobOpeningSerializer(serializers.ModelSerializer):
    # company = CompanySerializer()
    # reward = serializers.IntegerField(validators=[is_valid_reward])
    
    class Meta():
        model=JobOpening
        fields = '__all__'
    
    def create(self, validated_data):
        ## serializer.data로 넘어오면 주석범위로
        # company_id = validated_data.get("company")
        # validated_data["company"] = Company.objects.get(pk=company_id)
        return JobOpening.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        if validated_data.get("company"):
            raise serializers.ValidationError("company cannot be changed.")
        
        instance.position = validated_data.get('position', instance.position)
        instance.content = validated_data.get('content', instance.content)
        instance.tech = validated_data.get('tech', instance.tech)
        instance.reward = validated_data.get('reward', instance.reward)
        instance.save()
        return instance
    
    

