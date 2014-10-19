"Wil Wheaton Appreciation Guild"
==============

WWAG is a website that creates and uploads videos of entertaining game play to a 3rd party website for the public and premium viewers to enjoy. It's written in Python, with a bit of SQL, HTML5 (Jinja2) and CSS.

## Running the web app

There are two ways to run WWAG: the built-in WSGI server or CGI.

If possible, running the built-in WSGI server is much more performant than CGI:

    python run.py

Then open the browser at http://localhost:5000 to use the web application.

Otherwise, the `serve.py` file can be served in CGI (such as in IVLE), thanks to `CGIHandler` in `wsgiref`. You can optionally configure URL rewrites to generate "pretty URLs", but that's not possible in IVLE.

## Dependency management

As this project is designed to be fully self-contained, all packages have been vendored into the `/vendor` directory using pip:

    pip install -r requirements.txt -t vendor/

In `wwag/__init__.py`, the `vendor` and `lib` directory is added to the Python PATH:

    import sys, os
    # Add /vendor and /lib to python PATH
    sys.path.append(os.path.join(os.path.dirname(__file__), "../vendor"))
    sys.path.append(os.path.join(os.path.dirname(__file__), "../lib"))

## Utilities

To make system maintenance easier, there are a few built-in utilities in the web interface for easy-to-use management. For example, you can initialize the entire sqlite database or seed example data.

When the app is running for the first time, you will be redirected to `/utilities` to initialise the database schema and optionally load example data into the schema.

## User features

This WWAG implementation offers many features that exceed the minimum project requirements:

* **Flash messages**: All `POST` actions in the app will render flash messages after the redirections. This will allow users to receive immediate feedback on what they have done.
* **Basket**: This app uses the `ViewerOrder` data model to allow `Open` orders, which are orders that have not yet been checked out. Viewers can add more items to their Open orders later, effectively making them "shopping baskets".
* **Data validation**: All forms have sensible validations. If something is invalid an error message will be displayed clearly next to the user input.

## Technical features

WWAG follows several industry best practices and design patterns which may be out of scope in the course:

* **Templating**: WWAG uses jinja2 to render templates for HTML. Templates are entirely separated from Python code. 
* **Model-View-Controller**: WWAG generally follows the MVC pattern to separate business logic and presentation from request processing. Since this is a database project, we have avoided using ORM (which is very common in MVC apps) and thus the design pattern application is an incomplete one.
* **WSGI-compliant**: Built on the Flask microframework, WWAG is fully WSGI-compliant. This means that it can run efficiently in modern web servers. In fact, when being served in IVLE, the CGI environment will be transformed into WSGI during runtime.
* **Object-Oriented Design**: This project contains subclasses that inherit from the `Form` class in WTForms.
* **Semantic URLs**: Instead of query strings, every entity has a permanent and semantic URL. For example,
`/videos/4` means the video with `VideoID` = 4. This is generally more popular than query strings in modern web application development.

## External frameworks and libraries

This project wouldn't have been created so quickly and beautifully without several highly useful libraries:

* Flask (Python)
* Boostrap 3 (CSS)
* WTForms 2 (Python)

These libraries indirectly depend on the following which are also included in this application:

* Jinja2 (Python)

## Security

WWAG is an assignment project and not a commercial product. It's designed with functionality and proof of concepts in mind, not ncessarily security. While there are some essential security considerations in place, such as SQL Injection prevention and XSS protection, as well as cryptographically signed secure cookies and `SHA-256` hashed passwords, please do not run WWAG as a public web service in a mission-critical production server yet without a careful audit of the source code.

There's still a lot to do to make this app more secure, for example, by adding CSRF protection and HTTPS support.
