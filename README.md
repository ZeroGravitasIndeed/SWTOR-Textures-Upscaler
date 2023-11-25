## SWTOR Textures Upscaler
A fork of [**Hasib345's Texture_Upscaler**](https://github.com/Hasib345/Texture_Upscaler) ([Hasib345's Blender Market's Add-on's page](https://blendermarket.com/products/texture-upscaler---image-upscaler-for-blender)).


**This fork is a means to experiment with enhancing the textures of the Star Wars: The Old Republic (SWTOR) game (.dds format, which Blender can import but can't export, usually "packed" with multiple types of maps in a same image file).**

The idea is to have it export the images to be enhanced as PNG, WebP or JPG instead, saving them alongside the original .dds ones, and have the add-on assign them back instead. Also, it's about seeing ways to integrate the upscaler executable in other SWTOR-related tools (it's the first time I toy with a Blender add-on that interacts with a command line UI-executable).

As there are cases where the game's texture files will have very disparate data per channel that would suffer if enhanced as if they where full RGB images, I might have to investigate separating the channels into greyscale images, enhancing them, and combining them back 🤔.

ChangeLog:  
2023-11-25: fork creation.  

* * *

## Original Repository's README

Texture Upscaler is an AI-based texture-upscaler for Blender. This plugin allows you to upscale your textures with a single click. Textures will be upscaled 4x with little detail loss and artifacts using realesrgan ncnn vulkan.

Features:

*   Image Upscaling 4x
*   Include 6 models by default
*   Allows For replacing Textures in material with Upscaled textures
*   No dependencies required

**CONTRASTS**:

![](https://markets-rails.s3.amazonaws.com/cache/3edddf533059e52b5dd66cbc6cea6562.png)  

_Base Textures vs Upscaled Textures._

![](https://markets-rails.s3.amazonaws.com/cache/9b2369e8d061d05ab89aaf17cf6f207c.png)

_Upscaled Textures vs_ _Pbr Textures_ 

![](https://markets-rails.s3.amazonaws.com/cache/cce111b1de9fd1cdc19c1409ce66e5b9.png)

 _PBR Textures vs_ _Upscaled Textures_

INSTALLATION:

1.  Download the ZIP file 
2.  Within Blender, navigate to Edit > Preferences > Addons > Install
3.  Select the ZIP file
4.  Enable the addon by clicking on the box 
5.  Select Path for the Upscaled Textures in addon's preferences

**Usage:**

**Addon's Panel is present in  Image Editor > N-Panel > Texture Upscaler**

Navigate to the image editor window within Blender.

Open the texture you want to upscale.

Press 'N' to open the right-side toolbar

Navigate to the Texture Upscaler and click 'Texture Upscaler'

  

![](https://markets-rails.s3.amazonaws.com/cache/072502c9915f5c016d4f3feb412e5a48.png)

_Panel Preview_

  

About ESRGAN:

[Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) aims at developing Practical Algorithms for General Image/Video Restoration.  
We extend the powerful ESRGAN to a practical restoration application (namely, Real-ESRGAN), which is trained with pure synthetic data.  

[ncnn](https://github.com/Tencent/ncnn) is a high-performance neural network inference computing framework optimized for mobile platforms. ncnn is deeply considerate about deployment and uses on mobile phones from the beginning of design. ncnn does not have third party dependencies.

This addon is the [ncnn](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) [implementation](https://github.com/xinntao/Real-ESRGAN-ncnn-vulkan) of Real-ESRGAN in blender . 

This addon only works on Windows Operating Systems (For Now) .

**Additional links:**

If you want to add another model in the addon you can get the models for [this page](https://github.com/Hasib345/Custom_models) 

To add custom models to the addon there is an option in addon preferences.
