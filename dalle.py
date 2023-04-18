import os

import openai

openai.api_key = os.environ["OPENAI_API_KEY"]


def generate_image_and_return_url(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="256x256"
    )
    image_url = response['data'][0]['url']
    return image_url


if __name__ == "__main__":
    image = "Alas, a canine of noble birth embarked on a perilous journey, and in his travels, he chanced upon a fair maiden of the same breed, and thus, they fell in love and lived happily ever after"
    image_url = generate_image_and_return_url(image)
    print(image_url)
