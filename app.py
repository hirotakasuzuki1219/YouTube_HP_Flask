from flask import Flask, render_template
# from flask_mail import Mail, Message
# from flask_wtf import FlaskForm, RecaptchaField
# from wtforms import StringField, TextAreaField, SubmitField
# from wtforms.validators import DataRequired, Email
# from dotenv import load_dotenv
import os

# load_dotenv()

app = Flask(__name__)
# app.secret_key = os.urandom(24)

# # --- メール設定 ---
# app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_SSL'] = True
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
# app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_USERNAME')

# # --- reCAPTCHA 設定 ---
# app.config['RECAPTCHA_PUBLIC_KEY'] = os.getenv('RECAPTCHA_PUBLIC_KEY')
# app.config['RECAPTCHA_PRIVATE_KEY'] = os.getenv('RECAPTCHA_PRIVATE_KEY')

# mail = Mail(app)

# --- フォーム定義 ---
# class ContactForm(FlaskForm):
#     name = StringField('お名前', validators=[DataRequired()])
#     email = StringField('メールアドレス', validators=[DataRequired(), Email()])
#     message = TextAreaField('内容', validators=[DataRequired()])
#     recaptcha = RecaptchaField()
#     submit = SubmitField('送信')

# --- ルート ---
@app.route('/')
def home():
    return render_template('index.html')

# @app.route('/contact', methods=['GET', 'POST'])
# def contact():
#     form = ContactForm()
#     success = False
#     if form.validate_on_submit():
#         msg = Message(subject=f"[お問い合わせ] {form.name.data}",
#                       recipients=['自分の受信メール@gmail.com'])
#         msg.body = f"送信者: {form.name.data}\nメール: {form.email.data}\n内容:\n{form.message.data}"
#         mail.send(msg)
#         success = True
#     return render_template('contact.html', form=form, success=success)

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == "__main__":
    app.run()
