# Wiki - Built with Python and Flask

A wiki server that uses text files on the local filesystem to store page data. A location where anybody can look up and contribute known information about a television show they are interested in.

## Screenshots

![A screenshot of the front page of the wiki. Includes the page navigator and a feature to create a new page](screenshots/FrontPage.png)

![A screentshoot of a Page in the wiki,  where the user can see athe current cintent it has, and also access an edit form of the page or the history of changes made.](screenshots/ViewPage.png)
![Edit Form screentshot, where the suer can change or add to the current content, also needs to add a description of the change, their name and their email](screenshots/EditForm.png)
![View history of page, keeps track pf the changes made in a page. Includes date and hour it was made, description of the change, and nthe name and the email of the user that made it](screenshots/ViewHistory.png)

## Installation

This project has been tested with Python 3.7.3. To install the necessary dependencies, first create and activate a virtual environment.

```
# Create a directory to store virtual environments.
mkdir "$HOME/venvs"

# Create the virtual environment.
python3 -m venv "$HOME/venvs/dev"

# Activate the virtual environment.
# This must be done every time you open a terminal.
# You may want to add this to your .bashrc file.
source "$HOME/venvs/dev/bin/activate"
```

Install the necessary dependencies with pip.

```
pip install -r requirements.txt
```

## Usage

Run the web server.

```
./run-flask.sh
```

Access the wiki by opening a web preview browser tab on port 8080.

## License

Apache 2.0, see [LICENSE.txt](LICENSE.txt).
