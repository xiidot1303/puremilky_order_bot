from app.views import *


class FeedbackCreateView(APIView):
    async def post(self, request: AsyncRequest, *args, **kwargs):
        feedback_serializer = FeedbackSerializerByData(data=request.data)
        if await sync_to_async(feedback_serializer.is_valid)():
            # create Feedback by serializer
            await feedback_serializer.acreate(feedback_serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(feedback_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
