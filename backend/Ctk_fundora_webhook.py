from flask import Flask, request
import stripe
from database.Ctk_fundora_mySql_data_handler import update_user_to_premium

app = Flask(__name__)

stripe.api_key = "sk_test_YOUR_STRIPE_SECRET_KEY"  # Your test secret key 
endpoint_secret = "whsec_bwPqbpOhHUKTxU8MQJ3fvxQcErsauLHB"  # <-- paste the Signing secret from Stripe here https://dashboard.stripe.com/test/dashboard


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)

        if event['type'] == 'checkout.session.completed':
            customer_email = event['data']['object']['customer_details']['email']
            success = update_user_to_premium(customer_email)
            if success:
                print(f"Payment completed for: {customer_email} (user upgraded to premium).")
            else:
                print(f"Payment completed for: {customer_email}, but user not found in database.")

    except Exception as e:
        print("⚠️ Webhook error:", e)
        return "Bad signature", 400

    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)




# Activation and EXPLAINATION ON HOW FLASK FUNCTIONS

# ACTIVATION 
'''
Terminal 1 → Running Flask:
cd C:\Projects\Fundora
python -m backend.Ctk_fundora_webhook

Terminal 2 → Running ngrok:
ngrok http 5000

'''

# EXPLAINATION: 
'''
What you have just done
You built a small backend (Flask).
It’s a server that listens for Stripe’s messages at /webhook.
Think of it as: “When Stripe needs to tell me someone paid, call this address.”
You exposed that backend to the internet using ngrok.
Stripe can’t reach your local machine normally.
ngrok gives you a public URL (https://xxxx.ngrok-free.app) that forwards to your Flask app.
You told Stripe where to send payment notifications.
In the Stripe dashboard, you added a webhook endpoint (your ngrok URL).
Stripe now POSTs data there when a payment is successful.
You verified the message came from Stripe.
The “signing secret” ensures the request wasn’t faked.
If the secret is wrong or missing, you get 400 (bad request).
Now you’re seeing 200 OK → verified and accepted.
You confirmed it works.
When a test payment or “Send test event” runs, your Flask app prints the customer’s email.
This proves the full flow: Stripe → ngrok → Flask.
'''

# Flow Diagram 
'''
[Stripe]  --->  [ngrok tunnel: https://xxxx.ngrok-free.app/webhook]
                      |
                      v
             [Flask server @ localhost:5000]
                      |
                      v
        [update_user_to_premium() in MySQL]

'''