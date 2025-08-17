from flask import Flask, render_template, request, jsonify # type: ignore
from groq import Groq  # type: ignore
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
groq_api_key = os.getenv("GROQ_API_KEY")
sender_password = os.getenv("EMAIL_PASSWORD")
app = Flask(__name__)
client = Groq(api_key=groq_api_key)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_summary', methods=['POST'])
def generate_summary():
    transcript = request.form.get('transcript')
    prompt = request.form.get('prompt')

    if not transcript:
        return jsonify({"error": "Transcript is required."}), 400

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\nTranscript:\n{transcript}",
                }
            ],
            model="llama3-8b-8192",
        )

        summary = chat_completion.choices[0].message.content
        return jsonify({"summary": summary})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/send_email', methods=['POST'])
def send_email():
    recipients = request.form.get('recipients')
    summary = request.form.get('summary')

    if not recipients or not summary:
        return jsonify({"error": "Recipients and summary are required"}), 400
    sender_email = "22nn1a0575pavani@gmail.com"
    sender_password = sender_password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipients
    msg['Subject'] = "Meeting Summary"
    msg.attach(MIMEText(summary, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients.split(','), msg.as_string())
        server.quit()
        return jsonify({"success": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
