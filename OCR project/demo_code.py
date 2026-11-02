# Just a precaution the code is compatible upto py3.11.
# Higher versions are not tested yet.

from pathlib import Path
import sys

from PIL import Image, UnidentifiedImageError
import pytesseract
import translate # Not perfect translation


def extract_text_from_image(image_path: Path) -> str:
    with Image.open(image_path) as image:
        return pytesseract.image_to_string(image, lang="san").strip()


def main() -> None:
    image_path = input(
        "Enter an image path to scan (leave blank to translate the sample): "
    ).strip().strip('"')

    if image_path:
        try:
            text = extract_text_from_image(Path(image_path).expanduser())
        except FileNotFoundError:
            print(f"Image not found: {image_path}", file=sys.stderr)
            return
        except UnidentifiedImageError:
            print(f"Could not read the image file: {image_path}", file=sys.stderr)
            return
        except pytesseract.pytesseract.TesseractNotFoundError:
            print(
                "Tesseract ocr is not installed or is not on PATH. "
                "Install Tesseract ocr with sanskrit language (san) data.",
                file=sys.stderr,
            )
            return
        except pytesseract.pytesseract.TesseractError as error:
            print(
                f"OCR failed. Check that Tesseract has Sanskrit language (san) "
                f"data installed. Details: {error}",
                file=sys.stderr,
            )
            return
        except OSError as error:
            print(f"Image file access has failed(System error): {error}", file=sys.stderr)
            return
    else:
        text = "अद्य अहं मत्स्यं खादिष्यामि" # Sample

    if not text:
        print("No text was recognized in the image.", file=sys.stderr)
        return

    print("Original:", text)
    translator = translate.Translator(to_lang="en", from_lang="sa")
    print("Translated:", translator.translate(text))


if __name__ == "__main__":
    main()
