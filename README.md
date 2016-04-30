# RESTArt-JSONAPI-Demo

A JSON API demo based on RESTArt.


## Quickstart

1. Install the requirements

    ```
    $ cd restart-jsonapi-demo
    $ virtualenv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requirements.txt
    ```

2. Run the API

    ```
    (venv) $ restart blog.resources:api
    ```

3. Consume the API

    ```
    $ curl -i http://127.0.0.1:5000/articles
    $ curl -i http://127.0.0.1:5000/articles?include=author
    ```
