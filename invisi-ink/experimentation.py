import cv2

from utils.encode import encoding
from utils.decode import decoding

sh = 2
sw = 3

if __name__ == "__main__":
    raw_image = cv2.imread("./rinnegan.png")

    if raw_image is None:
        exit(0)

    message = "save save\nsave save\nsave save\nsave save\n"
    font_scale = 1

    encoded_image, text_image = encoding(raw_image, message, font_scale, sh, sw)

    # cv2.imshow("raw_image", raw_image)
    # cv2.imshow("text_image", text_image)
    # cv2.imshow("encoded_image", encoded_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    text_image_reconstructed = decoding(encoded_image, sh, sw)

    cv2.imshow("text_image_reconstructed", text_image_reconstructed)
    cv2.waitKey(0)
    cv2.destroyAllWindows()