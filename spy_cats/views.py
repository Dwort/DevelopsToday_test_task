import requests
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .serializers import CatRecordSerializer, CatSalarySerializer
from .models import Cats


class CreateCatAgent(APIView):
    CAT_API_URL = "https://api.thecatapi.com/v1/breeds"

    """
        If you want to add new cat, please send a request in this format!
        Example of body request:
        {
          "name": "cat_name",
          "year_of_exp": 1.2,
          "breed": "some_real_breed",
          "salary": "12345"
        }
        BE CAREFUL with BREED! You must write the real cat breed otherwise the data will not be saved.
    """

    def post(self, request):
        data = request.data
        breed = data.get("breed", None)

        if not breed:
            return Response({"detail": "The 'breed' field are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            response = requests.get(self.CAT_API_URL)
            if response.status_code != 200:
                return Response({"detail": "Failed to fetch data from TheCatAPI."},
                                status=status.HTTP_502_BAD_GATEWAY)

        except Exception as e:
            return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cat_api_data = response.json()

        breed_found = any(cat_api_breed['name'].lower() == breed.lower() for cat_api_breed in cat_api_data)

        if breed_found:
            serializer = CatRecordSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": True, "data": "New cat agency was added successfully"},
                                status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"success": False, "detail": "Breed not found. Create a cat with real breed!"},
                            status=status.HTTP_404_NOT_FOUND)


class GetAllCats(APIView):
    def get(self, request):
        cats = Cats.objects.all()
        serializer = CatRecordSerializer(cats, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SingleCatEdits(APIView):
    def get(self, request, cat_id):
        try:
            cat = Cats.objects.get(id=cat_id)
        except Cats.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CatRecordSerializer(cat)
        return Response(serializer.data, status=status.HTTP_200_OK)

    """
        Example of body request:
        {
            "salary": "777"
        }
    """

    def patch(self, request, cat_id):
        try:
            cat = Cats.objects.get(id=cat_id)
        except Cats.DoesNotExist:
            return Response({"error": "Cat not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CatSalarySerializer(cat, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cat_id):
        cat = Cats.objects.get(id=cat_id)
        if cat:
            cat.delete()
            return Response({"details": f"The cat with ID - {cat.id} was deleted successfully"},
                            status=status.HTTP_204_NO_CONTENT)
        return Response({"details": f"The cat with this ID - {cat.id} does not exist!"},
                        status=status.HTTP_400_BAD_REQUEST)

