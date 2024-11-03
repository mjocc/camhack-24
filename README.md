# CompSci Dating
*Cam hack 24 project*

## Setup guide

- Database needs to be manually initialised -- create a `db.sqlite3` file in the project root and initialise it by running the contents of `hangthedj/schema.sql` (this also inserts a small amount of example data) (e.g. `sqlite3 db.sqlite3 < hangthedj/schema.sql`)
- Create a `.env` file in the project root with `FLASK_SECRET_KEY` set to a random string and set `OPENAI_API_KEY` to a valid openai api key with credit

## Running

- Run the program with a development server via `flask --app hangthedj run --debug` (or `flash --app hangthedj run --host=0.0.0.0` to expose on local network) 