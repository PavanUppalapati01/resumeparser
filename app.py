from flask import Flask, render_template, request
import pymongo
import re

app = Flask(__name__)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["resume"]
collection = db["resume_data"]

@app.route('/', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        search_query = request.form['search']
        search_query2 = request.form['search1']
        search_query3=request.form['search2']
        keywords = search_query.split(',')
        keywords2 = search_query2.split(',')
        keywords3=search_query3.split(',')
        results = []
        
        # Search for documents with all skills present (case-insensitive)
        all_present_results = collection.find({
            "skills": {
                "$all": [re.compile(keyword, re.IGNORECASE) for keyword in keywords2]
            }
        })
        results.extend(all_present_results)

        # Search for documents with any skill present (case-insensitive)
        any_present_results = collection.find({
            "skills": {
                "$in": [re.compile(keyword, re.IGNORECASE) for keyword in keywords]
            }
        })
        results.extend(any_present_results)

        return render_template("index.html", results=results)

    return render_template('index.html')


if __name__ == '__main__':
    app.run()
