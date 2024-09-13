import datetime

from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from lunch_service.employee.models import Vote
from lunch_service.restaurant.models import Menu
from lunch_service.restaurant.serializers import MenuWithRestaurantSerializer

# Create your views here.


class TopVotedMenuView(APIView):
    permission_classes = []

    def get(self, request, *args, **kwargs):
        today = datetime.date.today()
        top_menu = (Vote.objects
                    .filter(date=today)
                    .values('menu')
                    .annotate(total_points=Sum('points'))
                    .order_by('-total_points')
                    .first())
        top_menu = Menu.objects.select_related('restaurant').get(pk=top_menu['menu'])
        if top_menu:
            serializer = MenuWithRestaurantSerializer(top_menu)
            return Response({"status": "success", "menu": serializer.data})
        return Response({"status": "error", "message": "No votes found"}, status=status.HTTP_404_NOT_FOUND)
