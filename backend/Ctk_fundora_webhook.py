from flask import Flask, request
import stripe

app = Flask(__name__)

stripe.api_key = "sk_test_YOUR_STRIPE_SECRET_KEY"  # Your test secret key 
endpoint_secret = "whsec_bwPqbpOhHUKTxU8MQJ3fvxQcErsauLHB"  # <-- paste the Signing secret from Stripe here https://dashboard.stripe.com/test/dashboard


@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except Exception as e:
        print("⚠️ Webhook error:", e)
        return "Bad signature", 400

    if event["type"] == "checkout.session.completed":
        print("💰 Payment completed for:", event["data"]["object"]["customer_details"]["email"])

    return "ok", 200

if __name__ == "__main__":
    app.run(port=5000)



# EXPLAINATION ON HOW FLASK FUNCTIONS
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
