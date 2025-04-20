from flask import Flask, render_template, request, session, redirect, url_for
import qrcode
import qrcode.image.svg
from io import BytesIO
from base64 import b64encode

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session handling

@app.route('/', methods=['GET', 'POST'])
def generateQR():
    base64_img = None  # Initialize base64_img to None

    # On POST request (form submission)
    if request.method == 'POST':
        data = request.form.get('link')

        # Only generate QR code if link is provided
        if data:
            memory = BytesIO()
            factory = qrcode.image.svg.SvgImage
            img = qrcode.make(data, image_factory=factory)

            img.save(memory)
            memory.seek(0)

            # Encode SVG data as base64
            base64_img = "data:image/svg+xml;base64," + b64encode(memory.getvalue()).decode('ascii')

            # Store QR code in session
            session['qr_code'] = base64_img

            # Redirect to the same page to clear POST data (to avoid re-submission on refresh)
            return redirect(url_for('generateQR'))

    # If the QR code is stored in the session, display it
    if 'qr_code' in session:
        base64_img = session['qr_code']
        # Clear the session after displaying QR code
        session.pop('qr_code', None)

    return render_template('index.html', data=base64_img)

if __name__ == '__main__':
    app.run(debug=True)
