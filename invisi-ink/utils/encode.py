import cv2
import numpy as np

sh = 2
sw = 3

def encoding(image, message, font_scale, sh, sw, color):
    print("converting image to 16 bits...")
    image = np.uint16(image)*255
    print("done converting image to 16 bits...")

    print("creating text image...")
    x0 = 50
    y0 = 50 * font_scale
    thickness = 2
    font_face = cv2.FONT_HERSHEY_SIMPLEX

    # create preview image
    h, w, _ = image.shape

    text_image = np.zeros((h, w), dtype=np.uint8)

    distance = 50
    sentences = message.splitlines()
    for index, sentence in enumerate(sentences):
        y = y0 + index * distance * font_scale
        text_image = cv2.putText(text_image, sentence, (x0, y), font_face, font_scale, color, thickness)

    print("done creating text image...")

    text_image = (text_image > 0).astype(np.int8)


    print("converting image to Y_CR_CB...")
    img_ycr_cb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
    Y, cr, cb = img_ycr_cb[:,:,0], img_ycr_cb[:,:,1], img_ycr_cb[:,:,2]
    print("done converting image to Y_CR_CB...")

    print("updating CR & CB...")
    # store the color
    bin_color = list(format(color[0], '08b'))+list(format(color[1], '08b'))+list(format(color[2], '08b'))
    
    # start = 9
    for x in range(cr.shape[0]):
        for y in range(cr.shape[1]):
            binary_cr = list(format(cr[x,y], '016b'))
            binary_cr[11] = text_image[x, y]
            binary_cr[12] = "0"
            binary_cr[13] = "1"
            binary_cr[14] = "1"
            binary_cr[15] = "1"
            
            cr[x,y]  = int("".join([str(bit) for bit in binary_cr]),2)

    exit = False
    index = 0
    for x in range(cb.shape[0]):
        if(exit):
            break
        for y in range(cb.shape[1]):
            if(index < len(bin_color)):
                
                binary_cb = list(format(cb[x,y], '016b'))

                binary_cb[11] = bin_color[index]

                binary_cb[12] = "0"
                binary_cb[13] = "1"
                binary_cb[14] = "1"
                binary_cb[15] = "1"
                
                index+=1
                
                cb[x,y]  = int("".join([str(bit) for bit in binary_cb]),2)
            else:
                exit = True
                break
    
  
    print("done updating CR & CB...")

    encoded_image = np.zeros(img_ycr_cb.shape, img_ycr_cb.dtype)
    encoded_image[:,:,0] = Y
    encoded_image[:,:,1] = cr
    encoded_image[:,:,2] = cb
    encoded_image = cv2.cvtColor(encoded_image, cv2.COLOR_YCrCb2BGR)

    return encoded_image, text_image

if __name__ == "__main__":
    image = cv2.imread("./rinnegan.png")

    if image is None:
        exit(0)
    
    message = "save save\nsave save\nsave save\nsave save\n"
    font_scale = 1

    encoded_image, text_image = encoding(image, message, font_scale, sh, sw)

    cv2.imshow("encoded image", encoded_image)
    cv2.imshow("text image", text_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()