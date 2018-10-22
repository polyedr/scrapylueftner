# scrapylueftner
Scrapy parser for Lueftner cruises website https://www.lueftner-cruises.com/en/river-cruises/cruise.html
This folder contains Scrapy https://scrapy.org/ spider together with auto-installation script for virtualenvironment, obtained from https://github.com/Yelp/venv-update/blob/master/venv_update.py. File requirements.txt contains virtual environment packages information. Output is placed at output.json.

1. 
Virtual environment automatic initialization. Python 3.4+. python3 venv-update.py venv= scrapylueftner pip-command= pip install pip==18.0

2. 
Activate the virtual environment for Scrapy, source ./scrapylueftner/bin/activate

3. 
Run the spider, scrapy crawl lueftner-cruises -o output.json
