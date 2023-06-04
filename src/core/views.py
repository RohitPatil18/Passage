from rest_framework import generics, status
from rest_framework.response import Response


class PostServiceAPIView(generics.GenericAPIView):
    response_status = status.HTTP_200_OK
    response_message = "Action was successfully performed."

    def get_response_payload(self, results):
        return {"success": True, "message": self.response_message, "data": {}}

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        results = self.process_request(request, serializer)
        return Response(
            self.get_response_payload(results),
            status=self.response_status,
        )

    def process_request(self, request, serializer):
        pass
