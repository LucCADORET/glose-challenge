# glose-challenge

The Glose recruitement challenge.

*Write an HTTP server, in Python, using only the standard lib (excluding the `http` module). The server should serve static files (its own code for example), and be able to list files like Apache does when serving a directory.
Please spend about 2 hours on this. The goal is obviously not to re-create Apache with all its functionalities but try to implement all the use-cases that you can think of and can cover in those 2 hours.*

## Requirements

Having python 3.7 is the only requirement, as this project only uses the standard lib

## Usage

Just start the server with python 3.7+:
`python main.py`
You can configure port and served directory from within the main.py code

## Features

- Starts an HTTP server on localhost, on a configurable port
- Parses requests from client (gets the method and the target URI)
- Returns the requested content: builds a directory page if the requested resource is a directory, returns file as text/html if it's a file (doesn't adapt to MIME type), returns 404 if nothing was found
- All files are served from a configurable folder (a "public" directory is published with this repo and is the default target folder)
- Uses asyncio, so multiple concurrent requests can be handled by the server