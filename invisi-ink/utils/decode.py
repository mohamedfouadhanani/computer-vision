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

  text_image = np.zeros((w, h, 3), dtype=np.uint8)
  text_image_grayscale = np.zeros((w, h), dtype=np.uint8)
  
  taille_max = text_image.shape[0] * text_image.shape[1]

  afterCoding = image

  afterCoding_ycrcb = cv2.cvtColor(afterCoding, cv2.COLOR_BGR2YCR_CB)

  Y2 = afterCoding_ycrcb[:, :, 0]
  cr2 = afterCoding_ycrcb[:, :, 1]
  cb2 = afterCoding_ycrcb[:, :, 2]
  
  index = 0
  exit_loop = False

  x = 0
  while x < (cr2.shape[0]) and exit_loop != True:
    y = 0
    while y < (cr2.shape[1]) and exit_loop != True:
        if index < taille_max:
            binary_cr = list(format(cr2[x,y], '016b'))
            text_image_grayscale[x, y] = binary_cr[11]
            index += 1
            y += 1
        else:
            exit_loop = True
    x += 1

  x = 0
  index_color = 0
  part_color = []
  while x < (cb2.shape[0]) and exit_loop != True:
    y = 0
    while y < (cb2.shape[1]) and exit_loop != True:
      if index_color < 24:
        binary_cb = list(format(cb2[x,y], '016b'))
        part_color.append(binary_cb[11])
        
        index_color += 1
        y += 1
      else:
        exit_loop = True
    x += 1

  color = [1, 1, 1]

  # get the color from bit sequence
  color[0]  = int("".join([str(bit) for bit in part_color[:8]]),2)
  color[1]  = int("".join([str(bit) for bit in part_color[8:16]]),2)
  color[2]  = int("".join([str(bit) for bit in part_color[16:24]]),2)

  text_image[:,:,0] = text_image_grayscale * color[0]
  text_image[:,:,1] = text_image_grayscale * color[1]
  text_image[:,:,2] = text_image_grayscale * color[2]
  
  text_image = cv2.cvtColor(text_image, cv2.COLOR_BGR2RGB)

  return text_image

if __name__ == "__main__":
    image = cv2.imread("./image.png")
    if image is None:
        exit(0)
        
    text_image = decoding(image, sh, sw)

    cv2.imshow("text image", text_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()