# from rest_framework import status
# from rest_framework import viewsets
# from rest_framework.response import Response

# from erp_customers.serializers.customer_create_serializer import (
#     CustomerCreateSerializer
# )

# from erp_customers.services.customer_application_service import (
#     CustomerApplicationService
# )



# class CustomerViewSet(
#     viewsets.ViewSet
# ):

#     def create(self, request):

#         serializer = (
#             CustomerCreateSerializer(
#                 data=request.data
#             )
#         )

#         serializer.is_valid(
#             raise_exception=True
#         )

#         customer = (
#             CustomerApplicationService.create(
#                 serializer.validated_data
#             )
#         )

#         return Response(
#             {
#                 "id": str(customer.id)
#             },
#             status=status.HTTP_201_CREATED
#         )

from rest_framework import viewsets, status
from rest_framework.response import Response
from sales_customers.models.customer_models import CustomerProfile
from sales_customers.serializers.customer_serializer import CustomerProfileSerializer
from sales_customers.services.customer_application_service import CustomerService

class CustomerProfileViewSet(viewsets.ModelViewSet):
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer

    def create(self, request, *args, **kwargs):
        profile = CustomerService.extend_partner_to_customer(request.data)
        serializer = self.get_serializer(profile)
        return Response(serializer.data, status=status.HTTP_201_CREATED)