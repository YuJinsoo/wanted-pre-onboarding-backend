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
    reward = serializers.IntegerField(validators=[is_valid_reward])
    
    class Meta():
        model=JobOpening
        fields = '__all__'
        
    def create(self, validated_data):
        ## serializer.data로 넘어오면 주석범위로
        # company_id = validated_data.get("company")
        # validated_data["company"] = Company.objects.get(pk=company_id)
        return JobOpening.objects.create(**validated_data)
    
    def is_valid_reward(self):
        if not isinstance(self.reward, int):
            return serializers.ValidationError("reward have to be integer.")
            
        if self.reward < 0 or self.reward > 2147483647:
            return serializers.ValidationError(f"reward have to be 0~2147483647. value: {self.reward}")


class UpdateJobOpeningSerializer(serializers.ModelSerializer):
    # company = serializers.ReadOnlyField(source='company.name')
    reward = serializers.IntegerField(validators=[is_valid_reward])
    
    class Meta():
        model=JobOpening
        exclude = ['company']
    
    def update(self, instance, validated_data):
        # for key in validated_data.keys():
        #     print(key)
        instance.position = validated_data.get('position', instance.position)
        instance.content = validated_data.get('content', instance.content)
        instance.tech = validated_data.get('tech', instance.tech)
        instance.reward = validated_data.get('reward', instance.reward)
        instance.country = validated_data.get('country', instance.country)
        instance.location = validated_data.get('location', instance.location)
        instance.save()
        return instance
    
    def is_valid_reward(self):
        if not isinstance(self.reward, int):
            return serializers.ValidationError("reward have to be integer.")
            
        if self.reward < 0 or self.reward > 2147483647:
            return serializers.ValidationError(f"reward have to be 0~2147483647. value: {self.reward}")
    
    

