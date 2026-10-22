PURE PYTHON IMAGE PROCESSOR
===========================

What this is
------------
A tiny image processor written in plain Python. No NumPy, OpenCV or Pillow.
An image is just a list of rows, and each row is a list of numbers from
0 (black) to 255 (white). Every function takes an image in and returns a NEW
image. The original is never changed.

How to run
----------
    python3 image_processor.py

Needs Python 3.10 or newer. Nothing to install.
The same output is saved in output.txt.

The test image (5x5)
--------------------
  10   10   10   10   10
  10   10   10  200  200
  10   10   10  200  255
  10   60   60   10   10
  10   60  120   10   10

It is deliberately lopsided (bright block top-right, dim block bottom-left).
A symmetrical image would look the same after a flip or rotation, and you
could not tell if the code worked.

Helper functions
----------------
make_image()   Returns the 5x5 test image.
show(t, img)   Prints a title and the image as aligned rows.
clamp(v)       Rounds a number and keeps it between 0 and 255.
get_pixel()    Reads a pixel, and handles the borders (see below).
convolve()     Slides a small kernel over the image (used by blur/edges).

1. Pixel-wise operations
------------------------
Each pixel is changed on its own. Neighbors do not matter.

invert(image)
  New value = 255 - old value. Dark becomes bright and bright becomes dark.
  The 255 pixel becomes 0. The 10s become 245.

adjust_brightness(image, amount)
  Adds amount to every pixel, then clamps to 0-255.
  +60: 200 becomes 255 (capped), 10 becomes 70.
  -60: 10 becomes 0 (floored), 255 becomes 195.

threshold(image, cutoff)
  Pixel >= cutoff becomes 255 (white), otherwise 0 (black).
  With cutoff 100, only 200, 255 and 120 stay white. This is a simple way
  to separate bright objects from the background.

2. Geometric operations
-----------------------
These move pixels around without changing their values.

flip_horizontal(image)
  Reverses each row. The bright block moves from top-right to top-left.

flip_vertical(image)
  Reverses the order of the rows. The bright block moves to the bottom.

rotate_90_clockwise(image)
  Turns the image a quarter turn clockwise. The bright block moves from
  top-right to bottom-right. The first column read bottom-to-top becomes
  the first row.

crop(image, top, left, height, width)
  Cuts out a rectangle. crop(img, 1, 1, 3, 3) keeps the middle 3x3 area.

3. Neighborhood operations
--------------------------
A kernel is a small grid of weights (here 3x3). For every pixel, we center
the kernel on it, multiply each weight by the pixel under it, and add up
the results. That sum is the new pixel value.

box_blur(image)
  Every weight is 1/9, so each pixel becomes the average of itself and its
  8 neighbors. Sharp changes get smoothed out. Look at the bright block:
  its edges fade into the dark area instead of jumping from 10 to 200.

edge_detect(image)
  Uses the Sobel kernels. One finds left-right changes, the other finds
  up-down changes. We add their absolute values. Flat areas become 0 (black)
  and areas where brightness changes sharply become large (white).
  The flat top-left corner is 0, and the edges of the bright block are 255.
  This is the basic idea behind lane-line detection.

Border handling (how and why)
-----------------------------
Pixels on the edge of the image have no neighbors on one side, so the kernel
would hang off the image. I used EDGE REPLICATION: if the kernel asks for a
pixel outside the image, get_pixel() returns the nearest pixel that is
inside the image.

Why I chose this:
- The output stays the same size as the input.
- Zero padding would treat the outside as black, which creates fake dark
  borders on a blur and fake edges on edge detection.
- Skipping the border pixels would shrink the image and lose data.
- Edge replication assumes the picture continues the way it looks at the
  border, which is the least surprising guess.

What the output shows
---------------------
The program prints the image BEFORE (the original at the top) and AFTER
each operation, so you can check everything by eye. Some things to verify:
- Invert: 10 -> 245 and 255 -> 0.
- Threshold: only the bright pixels are 255.
- Flip/rotate: follow the bright block (200, 200, 255) to see where it goes.
- Blur: values move toward their neighbors' average.
- Edge detection: 0 in flat regions, 255 along sharp changes.
The last section prints the original again and "Original unchanged: True".
This proves no function modified its input.

Files
-----
image_processor.py   The code
README.txt           This file
output.txt           Saved program output

Putting it on GitHub
--------------------
    git init
    git add image_processor.py README.txt output.txt
    git commit -m "Pure Python image processor"
    gh repo create image-processor --public --source=. --push
