import sys
import signal
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Message
import asyncio
import requests
import json
import os

try:
    webhookURL = os.getenv('WEBHOOK_URI')
except:
    print("Unable to fetch environment variable WEBHOOK_URI")
    raise

if webhookURL == None:
    print("No webhook URL provided")
    sys.exit(0)

print(webhookURL)

def signal_handler(signum, frame):
    print(f'\nReceived signal {signal.Signals(signum).name}')
    print('Shutting down server...')
    if 'controller' in globals():
        controller.stop()
    sys.exit(0)

if __name__ == '__main__':
    
    class EchoHandler:
        async def handle_DATA(self, server, session, envelope):
            # Prepare message for Discord
            message_content = f"New email from: {session.peer}\n```\n{envelope.content.decode('utf-8')}\n```"
            
            # Send to Discord
            payload = {
                "content": message_content
            }
            
            try:
                response = requests.post(
                    webhookURL,
                    data=json.dumps(payload),
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
            except Exception as e:
                print(f"Failed to send to Discord: {e}")
            
            return '250 Message accepted for delivery'

    def run():
        global controller
        handler = EchoHandler()
        controller = Controller(handler, hostname='0.0.0.0', port=25)
        print('SMTP Echo Server starting...')
        print('Listening on port 25')
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.signal(signal.SIGQUIT, signal_handler)
        
        try:
            controller.start()
            while True:
                asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))
        except Exception as e:
            print(f'\nError: {e}')
            controller.stop()
            sys.exit(1)

    run()