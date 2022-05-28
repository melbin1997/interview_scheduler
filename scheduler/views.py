import re

from django.db.models import Q
from django.forms import ValidationError
from django_filters.rest_framework import (ChoiceFilter, DjangoFilterBackend,
                                           FilterSet, NumberFilter)
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from .models import USER_TYPE, TimeSlot


class TimeSlotSerializer(ModelSerializer):
    class Meta:
        model = TimeSlot
        fields = '__all__'
    def validate(self, data):
        if(data['start_time'] > data['end_time']):
            raise ValidationError(message='Start time should be before end time')
        return data

class TimeSlotFilter(FilterSet):
    user_type = ChoiceFilter(choices = USER_TYPE)
    user_id = NumberFilter()

class TimeSlotViewSet(ModelViewSet):
    serializer_class = TimeSlotSerializer
    queryset = TimeSlot.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TimeSlotFilter



class AvailableTimeSlotView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        interviewer_id = request.query_params.get('interviewer_id')
        candidate_id = request.query_params.get('candidate_id')
        date_req = request.query_params.get('date')

        candidate_timeslot = list(qs.filter(date=date_req).filter(Q(user_id=candidate_id) & Q(user_type="CANDIDATE")).values_list('start_time','end_time'))
        interviewer_timeslot = list(qs.filter(date=date_req).filter(Q(user_id=interviewer_id) & Q(user_type="INTERVIEWER")).values_list('start_time','end_time'))

        result = []
        if candidate_timeslot and interviewer_timeslot:
            for (start_interviewer, end_interviewer) in interviewer_timeslot:
                interviewer_range = range(start_interviewer, end_interviewer)
                for (start_candidate, end_candidate) in candidate_timeslot:
                    candidate_range = range(start_candidate, end_candidate)
                    interviewer_range_set = set(interviewer_range)
                    result.extend([(elem_1, elem_1+1) for elem_1 in interviewer_range_set.intersection(candidate_range)])

        return Response(sorted(set(result)))

    def get_queryset(self):
        return TimeSlot.objects.all()
        