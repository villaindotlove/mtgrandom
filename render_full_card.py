from PIL import Image, ImageDraw, ImageFont

import os
from jinja2 import Template
from weasyprint import HTML, default_url_fetcher
from pdf2image import convert_from_path


def create_magic_card(card):
    """
    Creates a Magic the Gathering card image from provided card details.

    :param card: A dictionary containing card details.
    :return: File name of the created card image.
    """

    # Define HTML template for the card
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .card {
                background-color: white;
                border: 1px solid black;
                width: 63mm;
                height: 88mm;
                padding: 1px;
                box-sizing: border-box;
                font-size: 80%;  /* Adjust font size for entire card here */
            }
            .header, .type, .footer {
                border: 1px solid black;
                text-align: center;
                display: flex;
                justify-content: space-between;
                height: 8%;  /* Adjust this value as necessary */
                padding: 0 3px;
            }
            .footer {   
                font-size: 140%;  /* Adjust font size for footer here */
                padding: 0 7px;
            }
            .image-container {
                border: 1px solid black;
                height: 36%;  /* Adjust this value as necessary */
                object-fit: fill;
            }
            .image-container img {
                width: 100%;
                height: 100%;
                object-fit: cover;  /* Or "fill" */
            }
            .main-text {
                border: 1px solid black;
                height: 37%;  /* Adjust this value as necessary */
                padding: 0 3px;
            }
        </style>
    </head>
    <body>
        <div class="card">
            <div class="header">
                <span>{{card['name']}}</span>
                <span><img src="{{card['mana_cost']}}" /></span>
            </div>
            <div class="image-container">
                <img src="{{card['image']}}" />
            </div>
            <div class="type">{{card['type']}}</div>
            <div class="main-text">{{card['main_text']}}</div>
            <div class="footer">
                <span>TEST CARD</span>
                <span>{{card['power_toughness']}}</span>
            </div>
        </div>
    </body>
    </html>
    """

    # Create a Jinja2 template from the HTML template
    template = Template(html_template)

    # Render the card data with the template
    rendered_html = template.render(card=card)

    import logging
    logger = logging.getLogger('weasyprint')
    logger.addHandler(logging.FileHandler('weasyprint.log'))

    # The directory that contains your images
    base_url = os.path.abspath('images')

    # Create an HTML object with the rendered HTML
    html = HTML(string=rendered_html, base_url=base_url)
    # html = HTML(string=rendered_html, base_url=request.build_absolute_uri())

    with open("test.html", "w") as f:
        f.write(rendered_html)

    # Create a filename for the card pdf
    pdf_filename = f"{card['name']}.pdf"

    # Write the HTML to a pdf file
    html.write_pdf(pdf_filename)

    # Convert the first page of the PDF to an image
    images = convert_from_path(pdf_filename)

    # Save the first image to a file
    image_filename = f"{card['name']}.png"
    images[0].save(image_filename, 'PNG')

    # Remove the PDF file
    os.remove(pdf_filename)

    return image_filename


if __name__ == "__main__":
    images_dir = os.path.abspath('images')

    card = {
        "name": "Sample Card",
        "mana_cost": os.path.join(images_dir, "mana1.png"),
        "image": os.path.join(images_dir, "Mystic Oasis.png"),
        "type": "Creature - Human",
        "main_text": "Some main text",
        "power_toughness": "3/3",
    }

    image_filename = create_magic_card(card)

    print(f"Card image created: {image_filename}")

