from app.views import *
from app.services.client_service import *
from app.services.one_c_service import get_act_sverki
import base64
from io import BytesIO
from bot import NewsletterUpdate, InputFile
from bot.control.updater import application


class ReconciliationActView(APIView):
    async def post(self, request: AsyncRequest):
        start_period = request.data.get('start_period', None)
        end_period = request.data.get('end_period', None)
        client_id = request.data.get('client', None)

        client: Client = await Client.objects.aget(id=client_id)

        try:
            response = await get_act_sverki(client.uuid, start_period, end_period, region=client.region)
            pdf_base64 = response['data']
            pdf_data = base64.b64decode(pdf_base64)
            pdf_file = BytesIO(pdf_data)
            pdf_file.name = "file.pdf"
            bot_user: Bot_user = await get_bot_user_of_client(client)
            await application.update_queue.put(
                NewsletterUpdate(bot_user.user_id,
                                 f"Акт сверка:\n{start_period}-{end_period}",
                                 document=InputFile(pdf_file))
            )
            response = HttpResponse(pdf_data, content_type='application/pdf')
            response['Content-Disposition'] = 'inline; filename="generated.pdf"'
            return response

        except Exception as ex:
            import logging
            # logging.error(
            #
            # "ded", ex)
            return Response(status=500)
