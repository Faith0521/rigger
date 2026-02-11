# Copyright Epic Games, Inc. All Rights Reserved.

# Internal
from . import serializer_v1_2_0
from imp import reload

reload(serializer_v1_2_0)

SERIALIZERS = [serializer_v1_2_0.Serializer]
