# web-scraping-challenge- Mission to Mars
![image](https://user-images.githubusercontent.com/101610081/182186961-74b83f33-4531-4c23-acaf-4e8a2c8d8361.png)

Step 1 - Scraping
Complete your initial scraping using Jupyter Notebook, BeautifulSoup, Pandas, and Requests/Splinter.

Create a Jupyter Notebook file called mission_to_mars.ipynb and use this to complete all of your scraping and analysis tasks. The following outlines what you need to scrape.


NASA Mars News

Scrape the Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.

![image](https://user-images.githubusercontent.com/101610081/182187186-67fe92d6-8e86-4c35-a95c-81b94b77f101.png)


JPL Mars Space Images - Featured Image


Visit the url for the Featured Space Image site here.


Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.


Make sure to find the image url to the full size .jpg image.


Make sure to save a complete url string for this image.



Mars Facts


Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.


Use Pandas to convert the data to a HTML table string.

![image](https://user-images.githubusercontent.com/101610081/182187362-13b7c1f5-6702-4073-9d35-f68d2af6d38d.png)


Mars Hemispheres


Visit the astrogeology site here to obtain high resolution images for each of Mar's hemispheres.


You will need to click each of the links to the hemispheres in order to find the image url to the full resolution image.


Save both the image url string for the full resolution hemisphere image, and the Hemisphere title containing the hemisphere name. Use a Python dictionary to store the data using the keys img_url and title.


Append the dictionary with the image url string and the hemisphere title to a list. This list will contain one dictionary for each hemisphere.


Step 2 - MongoDB and Flask Application
Use MongoDB with Flask templating to create a new HTML page that displays all of the information that was scraped from the URLs above.


Start by converting your Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.


Next, create a route called /scrape that will import your scrape_mars.py script and call your scrape function.

Store the return value in Mongo as a Python dictionary.



Create a root route / that will query your Mongo database and pass the mars data into an HTML template to display the data.


Create a template HTML file called index.html that will take the mars data dictionary and display all of the data in the appropriate HTML elements. Use the following as a guide for what the final product should look like, but feel free to create your own design.

![image](https://user-images.githubusercontent.com/101610081/182187562-8742b16d-7a98-4edc-8400-61a5f38c3253.png)
