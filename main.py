import os

from Website import create_app

app = create_app()

# Define your custom filter function
def format_currency(value):
    if value == "None":
        return "0".format(value)
    return "{:,.2f}".format(value)

app.jinja_env.filters['format_currency'] = format_currency

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))
