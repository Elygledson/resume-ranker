import os
import fitz
import cv2
import easyocr
import numpy as np


class VisionTextProcessor:
    def __init__(self):
        self.reader = easyocr.Reader(['pt'])

    def extract_content(self, filepath: str) -> str:
        doc = None
        fulltext = ''

        try:
            doc = fitz.open(filepath)
            for page in doc:
                pix = page.get_pixmap(dpi=300)
                img_array = np.frombuffer(pix.samples, dtype=np.uint8).reshape(
                    pix.height, pix.width, pix.n
                )

                if pix.n == 4:
                    img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)

                results = self.reader.readtext(img_array)

                for _, text, _ in results:
                    fulltext += text + "\n"

            return fulltext.strip()

        finally:
            if doc:
                doc.close()
            if os.path.exists(filepath):
                os.remove(filepath)
