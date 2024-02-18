#!/home/jack/miniconda3/envs/cloned_base/bin/python
# filename ---  notes_app
from flask import Flask, request, render_template, redirect, url_for, send_from_directory, Response, send_file
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
app.use_static_path = True

# Configure your custom logger before basic logging configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Set the log level for the watchdog library to WARNING
logging.getLogger('watchdog').setLevel(logging.WARNING)

# Create a formatter for the log messages
# Log: time, level, message, path ahd line number
formatter = logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

# Create a file handler to write log messages to a file.
# If the log file gets over 10000 back it up and start a new app.log
file_handler = RotatingFileHandler(
    'Logs/app.log', maxBytes=10000, backupCount=1)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)
logger.debug("This is line: %d",29)

# Create a stderr handler to write log messages to sys.stderr
console_handler = logging.StreamHandler()
class WatchdogFilter(logging.Filter):
    def filter(self, record):
        # Filter out logs from the 'watchdog' library with level less than WARNING
        return not (record.name.startswith('watchdog.') and record.levelno < logging.WARNING)

# Add the filter to your logger
logger.addFilter(WatchdogFilter())# How do I ?
# open the file static/text/notes_app.txt
# split at the line "----------" 
# SEARCH THE TEXT FOR "uploads"
# print the results on an html page
@app.route('/notes')
def notes():
    with open('static/text/notes_app.txt') as f:
        text = f.read()
        #paragraph = text.split('----------')
        #search the paragraph for "uploads"

    return render_template('note_app_note.html', text=text)
 # split at the line "----------" and return the second part

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        if search_term:
            with open('static/text/notes_app.txt', 'r') as f:
                text = f.read()
                paragraphs = text.split('----------')

                # Filter paragraphs that contain the search term
                matching_paragraphs = [p for p in paragraphs if search_term in p]

            if matching_paragraphs:
                logger.debug("Matching Paragraphs: ", matching_paragraphs)
                return render_template('notes_app.html', text=matching_paragraphs)
            else:
                return render_template('notes_app.html', text=["No matching results."])
        else:
            return render_template('notes_app.html', text=["Enter a search term."])

    return render_template('notes_app.html', text=[])

@app.route('/search', methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        if search_term:
            with open('static/text/notes_app.txt', 'r') as f:
                text = f.read()
                paragraphs = text.split('----------')

                # Filter paragraphs that contain the search term
                matching_paragraphs = [p for p in paragraphs if search_term in p]

            if matching_paragraphs:
                logger.debug("Matching Paragraphs: ", matching_paragraphs)
                return render_template('notes_app.html', text=matching_paragraphs)
            else:
                return render_template('notes_app.html', text=["No matching results."])
        else:
            return render_template('notes_app.html', text=["Enter a search term."])

    return render_template('notes_app.html', text=[])

# Function to add ten dashes before and after the content
def format_content(content):
    separator = '----------\n'  # Define the separator
    formatted_content = f'{separator}{content.strip()}'  # Add separator before the content
    return formatted_content

@app.route('/append_notes', methods=['POST', 'GET'])
def append_notes():
    if request.method == 'POST':
        new_content = request.form.get('new_content', '').strip()
        if new_content:
            formatted_content = format_content(new_content)  # Format the content
            with open('static/text/notes_app.txt', 'a') as f:
                f.write(formatted_content)
            render_template('notes_app.html')
        else:
            return 'No content to append'

    return render_template('append_notes_app.html')

@app.route('/tree')
def tree():
    return render_template('NOTES_APPLICATION_tree.html')

if __name__ == '__main__':
    print("Starting Python Flask Server For Notes_App \n on port 5200")
    app.run(debug=True, host='0.0.0.0', port=5200)
