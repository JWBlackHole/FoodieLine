import os

from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent,
    LocationMessageContent
)

from module.model import MyModel
from module.user_locations import update_user_location, init_db

app = Flask(__name__)
llm = MyModel()

configuration = Configuration(access_token=os.environ['LINE_CHANNEL_ACCESS_TOKEN'])
handler       = WebhookHandler(os.environ['LINE_CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # print(event)
    # print(event.source.user_id)
    
    # ----- Get return message ----- #
    return_msg = ""
    try:
        response = llm.invoke(f"user_id: {event.source.user_id}, msg:{event.message.text}")
        return_msg = response["output"]
    except:
        return_msg = "Model Invoking Error."
        
    
    # ----- Send message to user ----- #
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=return_msg)]
            )
        )

@handler.add(MessageEvent, message=LocationMessageContent)
def handle_location_message(event):
    user_id   = event.source.user_id
    latitude  = event.message.latitude
    longitude = event.message.longitude
    # print(f"User Location: {latitude}, {longitude}")
    update_user_location(user_id, latitude, longitude)
    
    address = event.message.address
    # print(f"Address: {address}")

    return_msg = f"Thanks for sharing your location: {address}!"
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=return_msg)]
            )
        )

if __name__ == "__main__":
    init_db()
    app.run()