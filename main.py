from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
from openai import OpenAI
from lyzr import QABot

app = Flask(__name__)

load_dotenv()
my_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=my_key)

prompt=f"""
You are a customer service chatbot for amazon's return policy.
Your Task is to provide quick assistance to customer inquiries regarding amazon's return policy.
Familiarize yourself with Amazon's return policy thoroughly. This includes understanding what items are eligible for return, the timeframe for returns, and any special conditions for specific product categories.
In the first message you have to say only: How can I help you?
with the second message you have to give answer to their quesries.
"""

chat = QABot.pdf_qa(
        input_files=["Amazon-policy.pdf"],
        system_prompt=prompt

    )


def generate_answer(question):
    try:
        # chat = rag_bot()
        response = chat.query(question)
        return response.response
    except Exception as e:
        return f"Error generating answer: {e}"


@app.route('/chatgpt', methods=['POST'])
def chatgpt():
    incoming_que = request.values.get('Body', '').lower()
    print(incoming_que)

    answer = generate_answer(incoming_que)
    print(answer)

    bot_resp = MessagingResponse()
    msg = bot_resp.message()
    msg.body(answer)

    return str(bot_resp)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
