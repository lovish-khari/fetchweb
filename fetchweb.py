import os
import requests
from bs4 import BeautifulSoup
import jsbeautifier  # For beautifying JS and CSS

# Function to extract and beautify files
def extract_files(url, output_dir="./theagent"):
    # Check if the output directory exists, if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Get the website content
    response = requests.get(url)
    con = response.text
    soup = BeautifulSoup(con, "html.parser")

    print("Downloading files...")

    # JSBeautifier options
    beautify_options = jsbeautifier.default_options()

    # Extract and download CSS files
    for css in soup.find_all("link", rel="stylesheet"):
        css_url = css.get("href")
        if css_url.startswith("/"):
            css_url = url + css_url
        elif not css_url.startswith("http"):
            css_url = url + "/" + css_url
        css_filename = css_url.split("/")[-1].split("?")[0]  # Strip query string
        if not css_filename.endswith('.css'):  # Ensure it has a .css extension
            css_filename += '.css'
        css_path = os.path.join(output_dir, css_filename)
        css_response = requests.get(css_url)
        beautified_css = jsbeautifier.beautify(css_response.text, beautify_options)  # Beautify CSS
        with open(css_path, "w", encoding="utf-8") as f:
            f.write(beautified_css)
        print(f"Downloaded and beautified CSS: {css_filename}")

    # Extract and download JavaScript files
    for js in soup.find_all("script", src=True):
        js_url = js.get("src")
        if js_url.startswith("/"):
            js_url = url + js_url
        elif not js_url.startswith("http"):
            js_url = url + "/" + js_url
        js_filename = js_url.split("/")[-1].split("?")[0]  # Strip query string
        if not js_filename.endswith('.js'):  # Ensure it has a .js extension
            js_filename += '.js'
        js_path = os.path.join(output_dir, js_filename)
        js_response = requests.get(js_url)
        beautified_js = jsbeautifier.beautify(js_response.text, beautify_options)  # Beautify JavaScript
        with open(js_path, "w", encoding="utf-8") as f:
            f.write(beautified_js)
        print(f"Downloaded and beautified JS: {js_filename}")

    # Extract and download image files
    for img in soup.find_all("img", src=True):
        img_url = img.get("src")
        if img_url.startswith("/"):
            img_url = url + img_url
        elif not img_url.startswith("http"):
            img_url = url + "/" + img_url
        img_filename = img_url.split("/")[-1].split("?")[0]  # Strip query string
        img_path = os.path.join(output_dir, img_filename)
        img_response = requests.get(img_url)
        with open(img_path, "wb") as f:
            f.write(img_response.content)
        print(f"Downloaded Image: {img_filename}")

    # Save the prettified HTML file
    html_path = os.path.join(output_dir, "index.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(soup.prettify())  # Use prettify to format the HTML
    print("Downloaded and formatted HTML: index.html")

    print("All files have been downloaded, beautified, and saved to", output_dir)

# Main function to handle user input and call the extraction function
def main():
    print("Welcome! Please enter the URL of the website you want to extract files from:")
    url = input("URL: ")
    extract_files(url)

if __name__ == "__main__":
    main()