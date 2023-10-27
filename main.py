import base64
import hashlib
import time

from flask import Flask, request, jsonify, render_template, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to your MongoDB Atlas cluster
client = MongoClient("mongodb+srv://saurabhvishwakarma:Vishwakarma^(755)@cluster0.pje6o0d.mongodb.net/?retryWrites=true&w=majority")

# Access your database
db = client.url_shortener

# Access your collection (equivalent to table in SQL)
urls = db.urls


def generate_short_url(long_url):
    timestamp = str(int(time.time()))
    combined_str = long_url + timestamp
    hash_object = hashlib.sha256(combined_str.encode())
    hex_dig = hash_object.hexdigest()

    # Encode the hash to a shorter string
    short_url = (base64.urlsafe_b64encode(hex_dig.encode()).decode()[:8]).lower()

    return short_url


@app.route('/shorten', methods=['POST'])
def shorten_url():
    long_url = request.form.get('long_url')
    title = request.form.get('title')

    # Generate short URL
    short_url = generate_short_url(long_url)

    # Insert data into MongoDB
    urls.insert_one({
        "long_url": long_url,
        "short_url": short_url,
        "title": title,
        "hits": 0
    })
    return jsonify({'short_url': short_url})


@app.route('/search/<term>', methods=['GET'])
def search(term):
    results = list(urls.find({"title": {"$regex": term}}))

    response_data = []
    for result in results:
        response_data.append({
            "title": result["title"],
            "long_url": result["long_url"],
            "short_url": result["short_url"],
            "hits": result["hits"]
        })

    return jsonify({"results": response_data})


@app.route('/popular_url', methods=['GET'])
def get_popular_urls():
    # Query the database to get the most popular URLs based on hits
    results = list(urls.find().sort("hits", -1).limit(10))

    response_data = []
    for result in results:
        response_data.append({
            "title": result["title"],
            "long_url": result["long_url"],
            "short_url": result["short_url"],
            "hits": result["hits"]
        })

    return jsonify({"results": response_data})


@app.route('/<short_url>', methods=['GET'])
def redirect_to_original(short_url):
    result = urls.find_one({"short_url": short_url})

    if result:
        long_url = result["long_url"]

        # Update hit count
        urls.find_one_and_update({"short_url": short_url}, {"$inc": {"hits": 1}})

        return redirect(long_url)
    else:
        return "Short URL not found", 404


@app.route('/')
def short_url():
    return render_template('index.html')


@app.route('/search_terms')
def search_terms():
    return render_template('search_terms.html')


@app.route('/popular_urls')
def popular_urls():
    return render_template('popular_urls.html')



if __name__ == '__main__':
    app.run(debug=True)
