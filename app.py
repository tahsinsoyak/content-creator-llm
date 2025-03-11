import json
import os
import re
import time

from dotenv import load_dotenv
from flask import Flask, render_template, request
from groq import Groq


"""
This module defines a Flask web application for generating structured content using the Groq API.
The application supports generating content for different platforms such as blogs, Instagram, LinkedIn, and email.
Functions:
    about(): Renders the 'about' page.
    generate_response(system_prompt, user_prompt): Generates a response using the Groq API based on the provided system and user prompts.
    fix_json(json_string): Attempts to fix common JSON formatting issues in the provided string.
    index(): Handles the main page of the application, processes user input, and generates structured content.
Routes:
    /about: Renders the 'about' page.
    /: Handles the main page, processes POST requests to generate content, and renders the 'index' page.
"""


# .env dosyasından çevre değişkenlerini yükle
load_dotenv()

# Flask uygulamasını başlat
app = Flask(__name__)

# Çevre değişkenlerinden API anahtarını al
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise ValueError(
        "GROQ_API_KEY çevre değişkeni ayarlanmamış veya .env dosyasında eksik."
    )

# Groq istemcisini başlat
client = Groq(api_key=api_key)

# Sistem mesajlarını tanımla
SYSTEM_PROMPTS = {
    "blog": (
        "Kesinlikle bütün yanıtın *Türkçe* olmalı"
        "Sen profesyonel bir blog içerik yazarı ve SEO uzmanısın. "
        "Görevin, aşağıdaki JSON formatında bir blog taslağı oluşturmak "
        "return them *only* as a JSON object with no additional text"
        "Return *only* in the JSON format:"
        "{\n"
        '  "başlık": "",\n'
        '  "giriş": "",\n'
        '  "alt_başlıklar": [\n'
        "    {\n"
        '      "başlık": "",\n'
        '      "içerik": ""\n'
        "    }\n"
        "  ],\n"
        '  "sonuç": "",\n'
        '  "anahtar_kelime": [""],\n'
        '  "hashtag": [""],\n'
        '  "seo_odak_cümleleri": [""],\n'
        '  "bulletpoints": [""]\n'
        "}\n"
        "Başlıklar çarpıcı, giriş etkileyici, alt başlıklar bilgilendirici ve sonuç kısmı güçlü olmalıdır. "
        "SEO odaklı anahtar kelimeleri doğal bir şekilde ekle. Bullet point'ler ve düz yazı arasında net bir ayrım yap. "
        "Metni okunabilir ve ilgi çekici hale getir."
    ),
    "instagram": (
        "Kesinlikle bütün yanıtın *Türkçe* olmalı"
        "Sen Instagram içerik üretiminde uzmanlaşmış bir sosyal medya uzmanısın. "
        "Görevin, aşağıdaki JSON formatında bir Instagram içeriği oluşturmak"
        "return them *only* as a JSON object with no additional text"
        "Return *only* in the JSON format:"
        "{\n"
        '  "başlık": "",\n'
        '  "içerik": "",\n'
        '  "emoji": [""],\n'
        '  "çağrılar": [""],\n'
        '  "hashtag": [""],\n'
        '  "konum_etiket": ""\n'
        "}\n"
        "Başlık kısa ve dikkat çekici olmalıdır. Emojileri stratejik olarak yerleştir, etkili çağrılar ekle ve uygun hashtag'ler ile konum etiketleri kullan."
    ),
    "linkedin": (
        "Kesinlikle bütün yanıtın *Türkçe* olmalı"
        "Sen LinkedIn içerik oluşturucususun ve profesyonel bir gönderi hazırlıyorsun. "
        "Görevin, aşağıdaki JSON formatında bir içerik hazırlamak"
        "return them *only* as a JSON object with no additional text"
        "Return *only* in the JSON format:"
        "{\n"
        '  "giriş": "",\n'
        '  "ana_içerik": "",\n'
        '  "sonuç": "",\n'
        '  "hashtag": [""],\n'
        '  "çağrılar": [""],\n'
        '  "soru": ""\n'
        "}\n"
        "Giriş dikkat çekici, ana içerik değerli bilgiler veya ilham verici deneyimler içermeli, sonuç kısmı etkileyici olmalıdır. "
        "İlgili hashtag'ler ve etkileşimi artıracak çağrılar eklemeyi unutma."
    ),
    "email": (
        "Kesinlikle bütün yanıtın *Türkçe* olmalı"
        "Sen profesyonel bir e-posta metin yazarı ve tasarımcısın. "
        "Görevin, aşağıdaki JSON formatında bir e-posta taslağı hazırlamak"
        "return them *only* as a JSON object with no additional text"
        "Return *only* in the JSON format:"
        "{\n"
        '  "konu_satırı": "",\n'
        '  "kişisel_giriş": "",\n'
        '  "ana_içerik": "",\n'
        '  "harekete_geçirici_mesaj": "",\n'
        '  "kapanış": ""\n'
        "}\n"
        "Konu satırı dikkat çekici olmalı, giriş kişisel ve dostane, ana içerik kısa ve net, harekete geçirici mesaj (CTA) açık olmalıdır. "
        "Kapanış ise olumlu bir izlenim bırakacak şekilde tasarlanmalıdır."
    ),
}


@app.route("/about")
def about():
    """
    Renders the 'about' page of the web application.

    Returns:
        The rendered 'about.html' template.
    """
    return render_template("about.html")


def generate_response(system_prompt, user_prompt):
    """
    Generate a response using the Groq API.

    Args:
        system_prompt (str): The prompt provided by the system to guide the response generation.
        user_prompt (str): The prompt provided by the user to guide the response generation.

    Returns:
        str: The generated response content from the Groq API.
    """
    """Groq API kullanarak bir yanıt oluştur."""
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=1250,
    )
    return response.choices[0].message.content


def fix_json(json_string):
    """
    Attempts to correct common JSON formatting issues in a given string.

    This function performs several corrections on the input JSON string:
    1. Removes invalid '...' symbols.
    2. Eliminates trailing commas before closing brackets or braces.
    3. Checks for and fixes unclosed quotation marks.

    After attempting these corrections, it tries to parse the string into a
    Python object using the `json.loads` method. If successful, it returns
    the parsed data. If parsing fails, it returns a dictionary with an error
    message indicating the JSON decoding error.

    Args:
        json_string (str): The JSON string to be corrected and parsed.

    Returns:
        dict or list: The parsed JSON data if successful, or a dictionary
        containing an error message if parsing fails.
    """
    # 1. Geçersiz '...' sembollerini kaldır
    json_string = re.sub(r"\.\.\.", "", json_string)

    # 2. Fazla virgülleri kaldır (örneğin, listenin son elemanından sonra olanlar)
    json_string = re.sub(r",\s*([\]}])", r"\1", json_string)

    # 3. Açık kapanmayan tırnak işaretlerini kontrol et
    json_string = re.sub(r'(["\'])\s*([a-zA-Z0-9_]+)\s*\1', r'"\2"', json_string)

    try:
        data = json.loads(json_string)
        print("JSON başarıyla düzeltildi ve yüklendi.")
        return data
    except json.JSONDecodeError as e:
        print(f"Düzeltemedi: {e}")
        return {"error": f"JSON DecodeError: {e}"}


@app.route("/", methods=["GET", "POST"])
def index():
    """
    Handles the main page of the Flask application, processing user input to generate
    structured content using the Groq API.

    This function supports both GET and POST requests. For POST requests, it retrieves
    the content type and user prompt from the form data, generates a response using
    the Groq API, and attempts to parse the response into JSON format. If the JSON
    parsing fails, it tries to fix common JSON formatting issues. The structured
    content is then rendered on the 'index.html' template.

    Returns:
        Rendered HTML template with structured content and content type.
    """
    content = None
    json_data = {}  # Default empty response

    content_type = None  # Initialize content_type to be passed to the template

    if request.method == "POST":
        content_type = request.form.get("content_type")
        user_prompt = request.form.get("user_prompt")

        if content_type in SYSTEM_PROMPTS:
            system_prompt = SYSTEM_PROMPTS[content_type]
            for attempt in range(3):
                time.sleep(1)  # Wait for 1 second between attempts
                content = generate_response(system_prompt, user_prompt)
                print(f"Attempt {attempt + 1}: {content}")

                # Extract JSON from the response
                start = content.find("{")
                end = content.rfind("}") + 1

                if start != -1 and end != -1:
                    json_string = content[start:end]
                    try:
                        json_data = json.loads(json_string)
                        break  # JSON successfully parsed, exit the loop
                    except json.JSONDecodeError:
                        json_data = fix_json(json_string)
                else:
                    json_data = {"error": "Valid JSON not found."}

                if json_data.get("error") == "JSON could not be fixed" and attempt == 2:
                    # If on the final attempt and JSON could not be fixed
                    json_data = {
                        "error": "Failed to generate valid JSON after 3 attempts."
                    }

        else:
            content = "Invalid content type selected."

    return render_template(
        "index.html", structured_content=json_data, content_type=content_type
    )


if __name__ == "__main__":
    app.run(debug=True)
