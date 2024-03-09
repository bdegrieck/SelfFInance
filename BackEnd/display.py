from Website.views import post_data


class Display:
    def __init__(self, html_data: dict):
        self.html_data = html_data
        self.render_data(html_data=self.html_data)

    # sends df data to flask template
    def render_data(self, html_data: dict):
        for data, html in html_data.items():
            post_data(html_data=html)
