from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_webScrapper")

@app.route("/")
def home():
    destination_data = mongo.db.collection.find_one()
    return render_template("index.html" , mars_var = destination_data)


@app.route("/scrape")
def scrape():
    mars_var = scrape_mars.NASA_Mars_News()
    mars_var = scrape_mars.Featured_Image()
    mars_var = scrape_mars.Mars_Weather()
    mars_var = scrape_mars.Mars_Facts()
    mars_var = scrape_mars.Mars_Hemispheres()

    mongo.db.collection.update({}, mars_var, upsert=True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)