def make_image():
    return [
        [10, 10, 10, 10, 10],
        [10, 10, 10, 200, 200],
        [10, 10, 10, 200, 255],
        [10, 60, 60, 10, 10],
        [10, 60, 120, 10, 10],
    ]
 
 
def clamp(value):
    return max(0, min(255, int(round(value))))
 
 
def show(title, image):
    print(title)
    for row in image:
        print(" ".join(f"{pixel:4d}" for pixel in row))
    print()
 
 
def invert(image):
    return [[255 - pixel for pixel in row] for row in image]
 
 
def adjust_brightness(image, amount):
    return [[clamp(pixel + amount) for pixel in row] for row in image]
 
 
def threshold(image, cutoff):
    return [[255 if pixel >= cutoff else 0 for pixel in row] for row in image]
 
 
def flip_horizontal(image):
    return [row[::-1] for row in image]
 
 
def flip_vertical(image):
    return image[::-1]
 
 
def rotate_90_clockwise(image):
    return [list(row) for row in zip(*image[::-1])]
 
 
def crop(image, top, left, height, width):
    return [row[left:left + width] for row in image[top:top + height]]
 
 
def get_pixel(image, row, col):
    row = max(0, min(len(image) - 1, row))
    col = max(0, min(len(image[0]) - 1, col))
    return image[row][col]
 
 
def convolve(image, kernel):
    size = len(kernel)
    offset = size // 2
    result = []
    for r in range(len(image)):
        new_row = []
        for c in range(len(image[0])):
            total = 0
            for kr in range(size):
                for kc in range(size):
                    total += kernel[kr][kc] * get_pixel(image, r + kr - offset, c + kc - offset)
            new_row.append(total)
        result.append(new_row)
    return result
 
 
def box_blur(image):
    kernel = [[1 / 9] * 3 for _ in range(3)]
    return [[clamp(p) for p in row] for row in convolve(image, kernel)]
 
 
def edge_detect(image):
    sobel_x = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
    sobel_y = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    gx = convolve(image, sobel_x)
    gy = convolve(image, sobel_y)
    return [
        [clamp(abs(gx[r][c]) + abs(gy[r][c])) for c in range(len(image[0]))]
        for r in range(len(image))
    ]
 
 
def main():
    original = make_image()
    snapshot = [row[:] for row in original]
 
    show("ORIGINAL IMAGE", original)
 
    print("=== PIXEL-WISE OPERATIONS ===\n")
    show("Invert (255 - pixel)", invert(original))
    show("Brightness +60 (capped at 255)", adjust_brightness(original, 60))
    show("Brightness -60 (floored at 0)", adjust_brightness(original, -60))
    show("Threshold at 100 (>= 100 becomes 255, else 0)", threshold(original, 100))
 
    print("=== GEOMETRIC OPERATIONS ===\n")
    show("Flip horizontal (left <-> right)", flip_horizontal(original))
    show("Flip vertical (top <-> bottom)", flip_vertical(original))
    show("Rotate 90 degrees clockwise", rotate_90_clockwise(original))
    show("Crop: top=1, left=1, height=3, width=3", crop(original, 1, 1, 3, 3))
 
    print("=== NEIGHBORHOOD OPERATIONS (3x3 kernel, edge pixels repeated at borders) ===\n")
    show("Box blur", box_blur(original))
    show("Edge detection (Sobel)", edge_detect(original))
 
    print("=== ORIGINAL UNCHANGED CHECK ===\n")
    show("Original after all operations", original)
    print("Original unchanged:", original == snapshot)
 
 
if __name__ == "__main__":
    main()