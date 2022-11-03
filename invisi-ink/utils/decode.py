import cv2
import numpy as np

sh = 2
sw = 3

def isDivBy3(n):
 
  if(n%3 ==0):
    return True
  else:
    return False


def decoding(image, sh, sw):
    h, w, _ = image.shape
    h_b = int(h / sh)
    w_b = int(w / sw)

    text_image = np.zeros((w_b, h_b, 3), dtype=np.uint8)
    
    taille_max = text_image.shape[0] * text_image.shape[1] * 3 * 3

    afterCoding = image

    afterCoding_ycrcb = cv2.cvtColor(afterCoding, cv2.COLOR_BGR2YCR_CB)

    Y2 = afterCoding_ycrcb[:, :, 0]
    cr2 = afterCoding_ycrcb[:, :, 1]
    cb2 = afterCoding_ycrcb[:, :, 2]
    
    index = 0
    start = 9
    finish = 11
    partition = []
    x = 0
    exit_loop = False

    while x < (cr2.shape[0]) and exit_loop != True:
        y = 0
        while y < (cr2.shape[1]) and exit_loop != True:
            if index < taille_max:
                binary_cr = list(format(cr2[x,y], '016b'))
                partition.append(binary_cr[start:finish + 1])
                index += 1
                y += 1
            else:
                exit_loop = True
        x += 1

    x = 0
    while x < (cb2.shape[0]) and exit_loop != True:
        y = 0
        while y < (cb2.shape[1]) and exit_loop != True:
            if index < taille_max:
                binary_cb = list(format(cb2[x,y], '016b'))
                partition.append(binary_cb[start:finish + 1])

                index += 1
                y += 1
            else:
                exit_loop = True
        x += 1

    j = 0
    temp_list = []
    while(j < len(partition)):
        el1 = partition[j] + partition[j+1] + partition[j+2][:2]
        temp_list.append(int("".join(el1), 2))
        j += 3

    index_temp_list = 0

    for x in range(text_image.shape[0]):
        for y in range(text_image.shape[1]):
            for z in range(text_image.shape[2]):
                text_image[x,y,z] = temp_list[index_temp_list]
                index_temp_list += 1

    return text_image

if __name__ == "__main__":
    image = cv2.imread("./image.png")
    if image is None:
        exit(0)
        
    text_image = decoding(image, sh, sw)

    cv2.imshow("text image", text_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()