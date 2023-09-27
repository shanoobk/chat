import aiohttp
import json
from flask import Flask, request, render_template

app = Flask(__name__)

# Define your configuration settings here
app.config['ACCESS_TOKEN'] = 'EAAN3bcQzzWoBO2zAXSK5yuKuG5JnibrwVNI6vfaHZAIbqkOVFTn7zZADevUL1XZAJIO4ZBHbV1G4XcidbWppxYILPkoZBx8p6zZCddzzoOtlFTyMaYnwcPS8ZAba1qvDSfZAHSR9XKBgA1UYgOZCslWFZBb7cMDTskKiA3161oAOL4QX7bct5cYwHgUafbT3C0ZBruPidQ1ptZCigCcTLhsyAjktZB9wNNMV2ff4xBH8XgodjWltY4GaCk29t'
app.config['VERSION'] = 'v17.0'
app.config['PHONE_NUMBER_ID'] = '136827409506486'

@app.route('/', methods=['GET', 'POST'])
async def send_template_message():
    if request.method == 'POST':
        recipients = request.form.get('recipients')
        if recipients:
            recipient_list = recipients.split(',')  # Split the numbers by comma or your preferred delimiter
            success_messages = []
            error_messages = []
            
            for recipient in recipient_list:
                recipient = recipient.strip()  # Remove leading/trailing spaces
                template_data = get_templated_message_input(recipient)
                result = await send_message(template_data)
                
                if result == 'Message sent successfully.':
                    success_messages.append(f'Message sent to {recipient} successfully.')
                else:
                    error_messages.append(f'Failed to send message to {recipient}.')
            
            return render_template('index.html', success_messages=success_messages, error_messages=error_messages, show_form=True)
        else:
            return render_template('index.html', error_message='Recipient phone numbers are required.', show_form=True)
    return render_template('index.html', show_form=True)

async def send_message(data):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {app.config['ACCESS_TOKEN']}",
    }

    async with aiohttp.ClientSession() as session:
        url = f"https://graph.facebook.com/{app.config['VERSION']}/{app.config['PHONE_NUMBER_ID']}/messages"
        try:
            async with session.post(url, data=data, headers=headers) as response:
                if response.status == 200:
                    return 'Message sent successfully.'
                else:
                    return 'Failed to send message.'
        except aiohttp.ClientConnectorError as e:
            return f'Connection Error: {str(e)}'

def get_templated_message_input(recipient):
    return json.dumps({
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "apartment_rental",
            "language": {
                "code": "en_US"
            }
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
