
# Content Generator

This project is a Flask web application designed to generate structured content for various platforms using the Groq API. It supports generating content for blogs, Instagram, LinkedIn, and emails. The application provides a simple user interface where users can input prompts and receive platform-specific structured content in JSON format.

## Features

- **Platform-Specific Content Generation**:
  - Blog drafts with SEO-focused suggestions
  - Instagram posts with hashtags, emojis, and call-to-actions
  - LinkedIn posts with professional tone and engagement strategies
  - Emails with catchy subject lines and call-to-action messages
- **JSON Formatting**: Ensures all content is returned in a clean and structured JSON format.
- **Error Handling**: Attempts to fix common JSON formatting issues automatically.
- **Configurable API Key**: Uses environment variables for secure API key management.

## Requirements

- Python 3.10+
- Flask
- python-dotenv
- Groq API access

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/tahsinsoyak/content-creator-llm.git
    cd flask-groq-api
    ```

2. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use `venv\Scripts\activate`
    ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Set up environment variables:
    - Create a `.env` file in the root directory.
    - Add your Groq API key:
      ```env
      GROQ_API_KEY=your_api_key_here
      ```

5. Run the application:
    ```bash
    python app.py
    ```

6. Access the application in your browser at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project Structure

```plaintext
.
├── app.py                 # Main application file
├── templates/
│   ├── about.html         # About page template
│   └── index.html         # Main page template
├── static/                # Static assets (CSS, JS, images)
├── .env                   # Environment variables
├── requirements.txt       # Python dependencies
├── README.md              # Project documentation
```

## Routes

### `/`
- **Method**: `GET`, `POST`
- **Description**: Displays the main page. Accepts user input to generate content based on the selected platform.

### `/about`
- **Method**: `GET`
- **Description**: Renders the "About" page with information about the project.

## JSON Formats

### Blog Content
```json
{
  "başlık": "",
  "giriş": "",
  "alt_başlıklar": [
    {
      "başlık": "",
      "içerik": ""
    }
  ],
  "sonuç": "",
  "anahtar_kelime": [""],
  "hashtag": [""],
  "seo_odak_cümleleri": [""],
  "bulletpoints": [""]
}
```

### Instagram Content
```json
{
  "başlık": "",
  "içerik": "",
  "emoji": [""],
  "çağrılar": [""],
  "hashtag": [""],
  "konum_etiket": ""
}
```

### LinkedIn Content
```json
{
  "giriş": "",
  "ana_içerik": "",
  "sonuç": "",
  "hashtag": [""],
  "çağrılar": [""],
  "soru": ""
}
```

### Email Content
```json
{
  "konu_satırı": "",
  "kişisel_giriş": "",
  "ana_içerik": "",
  "harekete_geçirici_mesaj": "",
  "kapanış": ""
}
```

## Error Handling

### `fix_json`
The `fix_json` function:
- Removes invalid symbols (`...`).
- Fixes trailing commas.
- Ensures proper quotation marks.

If JSON parsing fails, it attempts to correct the format up to three times before returning an error.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contribution

Contributions are welcome! Please fork the repository and create a pull request with your changes.
