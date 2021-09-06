from flask import Flask, request
import os
import random
import requests

app = Flask("app")

# Repl provides these environment variables, we use it
# to construct the URL that this repl will be accessible on.
repl_owner = os.environ.get("REPL_OWNER")
repl_slug = os.environ.get("REPL_SLUG")
repl_url = f"https://{repl_slug}.{repl_owner.lower()}.repl.co"

TOKEN = os.environ.get("TOKEN")
HOST = os.environ.get("HOST", "https://whatsapp.turn.io")

@app.route("/")
def hello_world():
    return f"The Turn UI integration API endpoint is at {repl_url}/threads"


@app.route("/threads", methods=["POST"])
def threads():
  json = request.json
  number = random.randint(1, 6)
  cake_or_death = json['thread']['contact']['cake_or_death']
  wa_id = json['contacts'][0]['wa_id']

  # Send a custom reply at the end of the thread
  requests.post(url=f'{HOST}/v1/messages', headers={
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json'
  }, json={
    'type': 'text',
    'to': wa_id,
    'text': {
      'body': f'You chose {cake_or_death} and rolled {number}'
    }
  })

  if number > 3:
    bucket = 'cake'
  else:
    bucket = 'death'

  # Updates the contact profile with the scoring
  resp = requests.patch(url=f'{HOST}/v1/contacts/{wa_id}/profile', headers={
    'Authorization': f'Bearer {TOKEN}',
    'Content-Type': 'application/json',
    'Accept': 'application/vnd.v1+json'
  }, json={
    'cake_or_death_score': f'{bucket}'
  })

  return ''


app.run(host='0.0.0.0', port=8080)
