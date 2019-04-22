from SSIM_PIL import compare_ssim
from PIL import Image
from skimage import img_as_float
from skimage.measure import compare_psnr


if __name__ == '__main__':
    image1 = Image.open('./fog5-3-channel.png')
    i1 = image1.load()
    image2 = Image.open('./fog5-defogged.png')
    i2 = image2.load()
    ssim = compare_ssim(image1, image2)
    print("SSIM is " + str(ssim))

    i1 = img_as_float(image1)
    i2 = img_as_float(image2)
    psnr = compare_psnr(i1, i2)
    print("PSNR is "+str(psnr))
