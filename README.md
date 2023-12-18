# URL Shortener API Documentation

Welcome to the URL Shortener API documentation. This API allows you to shorten URLs and perform various operations with them. The base URL for this API is `https://urlshorterner-lng7.onrender.com/`.

## Shorten a URL
- **Endpoint**: `/shorten`
- **Method**: `POST`
- **Description**: Shorten a long URL to a unique, shorter URL.
- **Request Parameters**:
  - `long_url` (string, required): The long URL you want to shorten.
  - `title` (string, optional): An optional title or description for the URL.

**Example Request:**
```http
POST https://urlshorterner-lng7.onrender.com/shorten
Content-Type: application/json

{
  "long_url": "https://www.example.com",
  "title": "Example Website"
}

to view full documentation please visit https://drive.google.com/file/d/16CxI199zw3JJ02mdd_lHbFc8Fj3KNbHK/view
