from flask import Flask, render_template, request, send_file, url_for
from pdf2docx import Converter
import os
import uuid
from datetime import datetime
from gtts import gTTS
import qrcode
import io
import base64

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = os.path.join('static', 'results')

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RESULT_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pdf-to-word', methods=['GET', 'POST'])
def pdf_to_word():
    if request.method == 'POST':
        file = request.files['pdf']
        if file and file.filename.endswith('.pdf'):
            pdf_filename = f"{uuid.uuid4()}.pdf"
            docx_filename = f"{uuid.uuid4()}.docx"
            pdf_path = os.path.join(UPLOAD_FOLDER, pdf_filename)
            docx_path = os.path.join(RESULT_FOLDER, docx_filename)

            file.save(pdf_path)

            converter = Converter(pdf_path)
            converter.convert(docx_path, start=0, end=None)
            converter.close()

            return send_file(docx_path, as_attachment=True)

    return render_template('pdf_to_word.html')

@app.route('/text-tools', methods=['GET', 'POST'])
def text_tools():
    result = ''
    input_text = ''
    action = ''

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        action = request.form.get('action', '')

        if action == 'uppercase':
            result = input_text.upper()
        elif action == 'lowercase':
            result = input_text.lower()
        elif action == 'capitalize':
            result = input_text.title()
        elif action == 'remove_spaces':
            result = ' '.join(input_text.split())
        elif action == 'reverse':
            result = input_text[::-1]
        else:
            result = input_text

    return render_template('text_tools.html', input_text=input_text, result=result, action=action)

@app.route('/age-calculator', methods=['GET', 'POST'])
def age_calculator():
    age = None
    if request.method == 'POST':
        birth_date_str = request.form.get('birth_date')
        if birth_date_str:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d')
            today = datetime.today()

            years = today.year - birth_date.year
            months = today.month - birth_date.month
            days = today.day - birth_date.day

            if days < 0:
                months -= 1
                prev_month = (birth_date.month - 1) if birth_date.month > 1 else 12
                prev_year = birth_date.year if birth_date.month > 1 else birth_date.year - 1
                days_in_prev_month = (datetime(prev_year, prev_month + 1, 1) - datetime(prev_year, prev_month, 1)).days
                days += days_in_prev_month

            if months < 0:
                years -= 1
                months += 12

            age = {'years': years, 'months': months, 'days': days}

    return render_template('age_calculator.html', age=age)

@app.route('/text-to-speech', methods=['GET', 'POST'])
def text_to_speech():
    audio_file = None
    if request.method == 'POST':
        text = request.form.get('text', '').strip()
        lang = request.form.get('lang', 'ar')  # اللغة الافتراضية عربية
        if text:
            tts = gTTS(text, lang=lang)
            filename = f"speech_{uuid.uuid4()}.mp3"
            path = os.path.join(RESULT_FOLDER, filename)
            tts.save(path)
            print("Saved audio file at:", path)
            print("File size:", os.path.getsize(path), "bytes")
            audio_file = filename

    return render_template('text_to_speech.html', audio_file=audio_file)






from flask import Flask, render_template, request
import language_tool_python


# ... باقي الكود موجود عندك ...
from flask import Flask, render_template, request
import language_tool_python




@app.route('/qr-code', methods=['GET', 'POST'])
def qr_code():
    qr_img_data = None
    input_text = ''

    if request.method == 'POST':
        input_text = request.form.get('input_text', '')
        if input_text:
            # توليد QR Code
            qr = qrcode.QRCode(
                version=1,
                box_size=10,
                border=5
            )
            qr.add_data(input_text)
            qr.make(fit=True)
            img = qr.make_image(fill='black', back_color='white')

            # تحويل الصورة ل base64 لعرضها مباشرة في HTML
            buffer = io.BytesIO()
            img.save(buffer, format="PNG")
            img_str = base64.b64encode(buffer.getvalue()).decode("ascii")
            qr_img_data = f"data:image/png;base64,{img_str}"

    return render_template('qr_code.html', qr_img_data=qr_img_data, input_text=input_text)



from hijri_converter import convert


@app.route('/date-converter', methods=['GET', 'POST'])
def date_converter():
    result = None
    if request.method == 'POST':
        direction = request.form.get('direction')
        if direction == 'to_hijri':
            try:
                year = int(request.form.get('g_year'))
                month = int(request.form.get('g_month'))
                day = int(request.form.get('g_day'))
                hijri_date = convert.Gregorian(year, month, day).to_hijri()
                result = f"📅 التاريخ الهجري هو: {hijri_date.day}-{hijri_date.month}-{hijri_date.year}"
            except:
                result = "⚠️ تاريخ ميلادي غير صالح!"
        elif direction == 'to_gregorian':
            try:
                year = int(request.form.get('h_year'))
                month = int(request.form.get('h_month'))
                day = int(request.form.get('h_day'))
                gregorian_date = convert.Hijri(year, month, day).to_gregorian()
                result = f"📅 التاريخ الميلادي هو: {gregorian_date.day}-{gregorian_date.month}-{gregorian_date.year}"
            except:
                result = "⚠️ تاريخ هجري غير صالح!"
    return render_template('date_converter.html', result=result)





@app.route('/color-converter', methods=['GET', 'POST'])
def color_converter():
    # هنا يكون الكود اللي كتتعامل به مع تحويل RGB <-> HSL
    rgb_input = {'r': '', 'g': '', 'b': ''}
    hsl_input = {'h': '', 's': '', 'l': ''}
    rgb_result = None
    hsl_result = None
    error = ''

    if request.method == 'POST':
        conversion_type = request.form.get('conversion_type')
        if conversion_type == 'rgb_to_hsl':
            try:
                r = int(request.form.get('r'))
                g = int(request.form.get('g'))
                b = int(request.form.get('b'))

                if not all(0 <= x <= 255 for x in (r,g,b)):
                    error = 'قيم RGB يجب أن تكون بين 0 و 255'
                else:
                    h, s, l = rgb_to_hsl(r, g, b)
                    hsl_result = {'h': h, 's': s, 'l': l}
                    rgb_input = {'r': r, 'g': g, 'b': b}
            except:
                error = 'رجاءً أدخل قيم صحيحة لألوان RGB'

        elif conversion_type == 'hsl_to_rgb':
            try:
                h = int(request.form.get('h'))
                s = int(request.form.get('s'))
                l = int(request.form.get('l'))

                if not (0 <= h <= 360 and 0 <= s <= 100 and 0 <= l <= 100):
                    error = 'قيم HSL: H (0-360), S و L (0-100)'
                else:
                    r, g, b = hsl_to_rgb(h, s, l)
                    rgb_result = {'r': r, 'g': g, 'b': b}
                    hsl_input = {'h': h, 's': s, 'l': l}
            except:
                error = 'رجاءً أدخل قيم صحيحة لألوان HSL'

    return render_template('color_converter.html', rgb_input=rgb_input, hsl_input=hsl_input,
                           rgb_result=rgb_result, hsl_result=hsl_result, error=error)




@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    expression = ''
    result = None
    error = None

    if request.method == 'POST':
        expression = request.form.get('expression', '')

        try:
            # لتجنب المخاطر، استخدم مكتبة ast لتقييم التعبير بأمان:
            import ast
            import operator as op

            # دعم العمليات الحسابية البسيطة فقط
            allowed_operators = {
                ast.Add: op.add,
                ast.Sub: op.sub,
                ast.Mult: op.mul,
                ast.Div: op.truediv,
                ast.Pow: op.pow,
                ast.USub: op.neg,
            }

            def eval_expr(node):
                if isinstance(node, ast.Num):  # رقم
                    return node.n
                elif isinstance(node, ast.BinOp):  # عملية حسابية
                    left = eval_expr(node.left)
                    right = eval_expr(node.right)
                    oper = allowed_operators[type(node.op)]
                    return oper(left, right)
                elif isinstance(node, ast.UnaryOp):  # عملية أحادية مثل السالب
                    operand = eval_expr(node.operand)
                    oper = allowed_operators[type(node.op)]
                    return oper(operand)
                else:
                    raise TypeError("عملية غير مسموحة")

            tree = ast.parse(expression, mode='eval')
            result = eval_expr(tree.body)
        except Exception:
            error = "عذراً، المعادلة غير صحيحة أو تحتوي على رموز غير مدعومة."

    return render_template('calculator.html', expression=expression, result=result, error=error)




from PIL import Image

@app.route('/image-to-icon', methods=['GET', 'POST'])
def image_to_icon():
    icon_url = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            filename = f"{uuid.uuid4()}.ico"
            path = os.path.join(RESULT_FOLDER, filename)

            img = Image.open(file)
            img = img.resize((64, 64))  # يمكنك تغيير الحجم حسب الحاجة
            img.save(path, format='ICO')

            icon_url = url_for('static', filename='results/' + filename)

    return render_template('icon_converter.html', icon_url=icon_url)




from PIL import Image
import os
import uuid

@app.route('/image-compress', methods=['GET', 'POST'])
def image_compress():
    image_url = None
    original_size = None
    compressed_size = None

    if request.method == 'POST':
        file = request.files.get('image')
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            filename = f"{uuid.uuid4()}.jpg"
            path_original = os.path.join(UPLOAD_FOLDER, filename)
            path_compressed = os.path.join(RESULT_FOLDER, filename)

            file.save(path_original)
            original_size = round(os.path.getsize(path_original) / 1024, 2)  # KB

            # ضغط الصورة باستخدام PIL
            img = Image.open(path_original)
            img_rgb = img.convert("RGB")  # لضمان التنسيق الصحيح
            img_rgb.save(path_compressed, format="JPEG", quality=50, optimize=True)

            compressed_size = round(os.path.getsize(path_compressed) / 1024, 2)  # KB
            image_url = url_for('static', filename='results/' + filename)

    return render_template('image_compressor.html',
                           original_size=original_size,
                           compressed_size=compressed_size,
                           image_url=image_url)




@app.route('/equation-solver', methods=['GET', 'POST'])
def equation_solver():
    result = None
    equation_type = None
    a = b = c = None

    if request.method == 'POST':
        equation_type = request.form.get('equation_type')
        try:
            a = float(request.form.get('a'))
            b = float(request.form.get('b'))

            if equation_type == 'linear':
                if a == 0:
                    result = "⚠️ لا يمكن حل المعادلة لأن a = 0"
                else:
                    x = -b / a
                    result = f"✅ الحل: x = {x:.2f}"
            elif equation_type == 'quadratic':
                c = float(request.form.get('c', 0))
                delta = b**2 - 4*a*c
                if delta < 0:
                    result = "❌ لا يوجد حل حقيقي (Δ < 0)"
                elif delta == 0:
                    x = -b / (2*a)
                    result = f"✅ حل واحد: x = {x:.2f}"
                else:
                    x1 = (-b + delta**0.5) / (2*a)
                    x2 = (-b - delta**0.5) / (2*a)
                    result = f"✅ حلان: x₁ = {x1:.2f}, x₂ = {x2:.2f}"
        except:
            result = "⚠️ تأكد من إدخال القيم بشكل صحيح"

    return render_template('equation_solver.html', result=result, equation_type=equation_type, a=a, b=b, c=c)





from email_validator import validate_email, EmailNotValidError
import dns.resolver


def check_mx_record(domain):
    try:
        answers = dns.resolver.resolve(domain, 'MX')
        return len(answers) > 0
    except Exception:
        return False

@app.route('/email', methods=['GET', 'POST'])
def email_check():
    result = None
    email = ''
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        if not email:
            result = ('error', 'المرجو إدخال بريد إلكتروني')
        else:
            try:
                # التحقق من صحة البريد إلكتروني (صيغة)
                valid = validate_email(email)
                domain = valid.domain
                
                # التحقق من سجل MX
                if check_mx_record(domain):
                    result = ('success', 'البريد الإلكتروني صحيح وصالح')
                else:
                    result = ('error', 'الدومين الخاص بالبريد الإلكتروني ما عندوش سجلات MX')
            except EmailNotValidError as e:
                result = ('error', f'صيغة البريد الإلكتروني غير صحيحة: {str(e)}')

    return render_template('email.html', result=result, email=email)







if __name__ == '__main__':
    app.run(debug=True)
