import os

from Website import create_app
from Website.views import format_currency

app = create_app()
app.jinja_env.filters['format_currency'] = format_currency

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'),
            port=int(os.getenv('PORT', 4444)))
