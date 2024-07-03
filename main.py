import os
import argparse
from PIL import Image, ImageDraw, ImageFont


def add_text_watermark(image_path, text, position, font_path, font_size, output_path):
    image = Image.open(image_path).convert("RGBA")
    watermark = Image.new("RGBA", image.size)

    draw = ImageDraw.Draw(watermark)
    font = ImageFont.truetype(font_path, font_size)
    text_width, text_height = draw.textsize(text, font)

    if position == 'top-left':
        pos = (10, 10)
    elif position == 'top-right':
        pos = (image.width - text_width - 10, 10)
    elif position == 'bottom-left':
        pos = (10, image.height - text_height - 10)
    elif position == 'bottom-right':
        pos = (image.width - text_width - 10, image.height - text_height - 10)
    else:
        pos = ((image.width - text_width) // 2, (image.height - text_height) // 2)

    draw.text(pos, text, font=font, fill=(255, 255, 255, 128))

    watermarked_image = Image.alpha_composite(image, watermark)
    watermarked_image = watermarked_image.convert("RGB")  # Remove alpha for saving in jpg format
    watermarked_image.save(output_path)


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


def main():
    parser = argparse.ArgumentParser(description="Add watermark to an image")
    parser.add_argument("image", help="Path to the input image")
    parser.add_argument("--text", help="Text watermark to add")
    parser.add_argument("--text-size", type=int, default=36, help="Font size of the text watermark")
    parser.add_argument("--font", default="arial.ttf", help="Path to the font file for text watermark")
    parser.add_argument("--watermark", help="Path to the watermark image")
    parser.add_argument("--position", choices=['top-left', 'top-right', 'bottom-left', 'bottom-right', 'center'],
                        default='bottom-right', help="Position of the watermark")
    parser.add_argument("output", help="Path to the output image")

    args = parser.parse_args()

    if args.text:
        add_text_watermark(args.image, args.text, args.position, args.font, args.text_size, args.output)
    elif args.watermark:
        add_image_watermark(args.image, args.watermark, args.position, args.output)
    else:
        print("Error: You must specify either --text or --watermark")
        parser.print_help()


if __name__ == "__main__":
    main()
