from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Missions, Target
from spy_cats.models import Cats
from .serializers import MissionSerializer


class CreateMissionAndTargets(APIView):
    """
        Example of body request:
        {
            "cat_name": "Tom",
            "notes": "Explore new territories.",
            "complete": false,
            "targets": [
                {
                    "name": "Target One",
                    "country": "USA",
                    "notes": "Explore hidden spots.",
                    "complete": false
                },
                {
                    "name": "Target Two",
                    "country": "Canada",
                    "notes": "Find sunny places.",
                    "complete": false
                }
            ]
        }
    """
    def post(self, request):
        serializer = MissionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllMission(APIView):
    def get(self, request):
        missions = Missions.objects.all()
        serializer = MissionSerializer(missions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MissionEdits(APIView):
    def get(self, request, mission_id):
        try:
            mission = Missions.objects.get(id=mission_id)
        except Missions.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        serializer = MissionSerializer(mission)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, mission_id):
        try:
            mission = Missions.objects.get(id=mission_id)
        except Missions.DoesNotExist:
            return Response({"details": "Mission does not exist."}, status=status.HTTP_404_NOT_FOUND)

        if mission.cat is None:
            mission.delete()
            return Response(
                {"details": "The mission was deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

        return Response({"details": "The mission has an executor! Cannot be deleted."},
                        status=status.HTTP_400_BAD_REQUEST)


class AssignCatToMission(APIView):
    """
        Example of body request:
        {
            "id": 3,
            "cat_name": "cat name"
        }
    """

    def patch(self, request):
        mission_id = request.data['id']
        cat_name = request.data['cat_name']

        if not mission_id or not cat_name:
            return Response({"details": "Mission ID and cat name are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            mission = Missions.objects.get(id=mission_id)
            cat = Cats.objects.get(name=cat_name)
        except Missions.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Cats.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if mission.cat:
            return Response({"details": "This mission already has an executor! Choose a mission without an executor"},
                            status=status.HTTP_400_BAD_REQUEST)

        if Missions.objects.filter(cat=cat).exists():
            return Response({"details": "This cat already has an active mission."},
                            status=status.HTTP_400_BAD_REQUEST)

        mission.cat = cat
        mission.save()

        return Response({"details": f"Cat '{cat_name}' successfully assigned to mission {mission.id}."},
                        status=status.HTTP_200_OK)


class UpdateTargetMark(APIView):
    def patch(self, request, target_id):

        mark = request.query_params.get('mark')
        if mark is None:
            return Response({"error": "New mark of completing are needed"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            target = Target.objects.get(id=target_id)
        except Target.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_404_NOT_FOUND)

        try:
            target.complete = bool(mark)
            target.save()
        except ValueError as e:
            return Response(f"Mark must be 'True' or 'False' nothing other.\n{str(e)}",
                            status=status.HTTP_400_BAD_REQUEST)

        # Set mission complete status to True if all targets are done (True).
        if target.mission:
            all_completed = target.mission.target_set.all().filter(complete=False).count() == 0
            if all_completed:
                target.mission.complete = True
                target.mission.save()

        return Response({"details": "Mark was changed successfully!"}, status=status.HTTP_200_OK)


class UpdateTargetNotes(APIView):

    """
        Example of body request:
        {
            "notes": "new notes"
        }
    """

    def patch(self, request, target_id):
        new_notes = request.data['notes']
        try:
            target = Target.objects.get(id=target_id)
        except Target.DoesNotExist as e:
            return Response({"details": str(e)}, status=status.HTTP_404_NOT_FOUND)

        if target.mission.complete:
            return Response({"details": "You can not add new notes to the task. Mission is completed"},
                            status=status.HTTP_400_BAD_REQUEST)
        if target.complete:
            return Response({"details": "You can not add new notes to the task. Target is completed"},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            target.notes = new_notes
            target.save()

            return Response({"details": "Target updated successfully!"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
