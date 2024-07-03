import os
import argparse
from PIL import Image


def print_logo():
    logo = r"""
   ___  __        __         _      __     __                         __          
  / _ \/ /  ___  / /____    | | /| / /__ _/ /____ ______ _  ___ _____/ /_____ ____
 / ___/ _ \/ _ \/ __/ _ \   | |/ |/ / _ `/ __/ -_) __/  ' \/ _ `/ __/  '_/ -_) __/
/_/  /_//_/\___/\__/\___/   |__/|__/\_,_/\__/\__/_/ /_/_/_/\_,_/_/ /_/\_\\__/_/   
    """
    print("--------------------------------------------------")
    print(logo)
    print("Photo Watermarker")
    print("Made with 💜 by Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/photo-watermarker/")
    print("--------------------------------------------------")


def add_image_watermark(image_path, watermark_path, position, output_path):
    image = Image.open(image_path).convert("RGBA")
    watermark = Image.open(watermark_path).convert("RGBA")

    if position == 'top-left':
        pos = (10, 10)
    elif position == 'top-right':
        pos = (image.width - watermark.width - 10, 10)
    elif position == 'bottom-left':
        pos = (10, image.height - watermark.height - 10)
    elif position == 'bottom-right':
        pos = (image.width - watermark.width - 10, image.height - watermark.height - 10)
    else:
        pos = ((image.width - watermark.width) // 2, (image.height - watermark.height) // 2)

    transparent = Image.new('RGBA', (image.width, image.height), (0, 0, 0, 0))
    transparent.paste(image, (0, 0))
    transparent.paste(watermark, pos, mask=watermark)

    watermarked_image = Image.alpha_composite(image, transparent)
    watermarked_image = watermarked_image.convert("RGB")  # Remove alpha for saving in jpg format
    watermarked_image.save(output_path)


def prompt_user_for_inputs():
    image_path = input("Enter the path to the input image: ")
    watermark_path = input("Enter the path to the watermark image: ")
    position = input(
        "Enter the position for the watermark (top-left, top-right, bottom-left, bottom-right, center): ").strip().lower() or 'bottom-right'
    output_path = input("Enter the path to save the output image (default is output.jpg): ") or 'output.jpg'

    return image_path, watermark_path, position, output_path


def main():
    print_logo()

    parser = argparse.ArgumentParser(description="Add an image watermark to an image")
    parser.add_argument("image", nargs='?', help="Path to the input image")
    parser.add_argument("--watermark", help="Path to the watermark image")
    parser.add_argument("--position", choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                        default='bottom-right', help="Position of the watermark")
    parser.add_argument("--output", help="Path to the output image", default="output.jpg")

    args = parser.parse_args()

    if not args.image:
        image_path, watermark_path, position, output_path = prompt_user_for_inputs()
    else:
        image_path = args.image
        watermark_path = args.watermark
        position = args.position
        output_path = args.output

    if watermark_path:
        add_image_watermark(image_path, watermark_path, position, output_path)
    else:
        print("Error: You must specify --watermark")
        parser.print_help()


if __name__ == "__main__":
    main()
