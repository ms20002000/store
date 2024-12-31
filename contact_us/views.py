from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import ContactUsSerializer


class ContactUsView(APIView):
    
    def post(self, request):
        serializer = ContactUsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({
                "message": "Your message sent successfully"
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)