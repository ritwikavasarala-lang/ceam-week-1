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

 
 
def ask_number(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a whole number.\n")


def print_commands():
    print("Commands: invert, brightness, threshold, hflip, vflip, rotate, crop, blur, edge, exit\n")


def main():
    original = make_image()
    show("ORIGINAL IMAGE", original)
    print_commands()

    while True:
        command = input("Enter a command: ").strip().lower()
        print()

        match command:
            case "invert":
                result = invert(original)
                title = "Invert"
            case "brightness":
                amount = ask_number("Brightness amount (for example 60 or -60): ")
                result = adjust_brightness(original, amount)
                title = f"Brightness {amount}"
            case "threshold":
                cutoff = ask_number("Threshold cutoff (0-255): ")
                result = threshold(original, cutoff)
                title = f"Threshold at {cutoff}"
            case "hflip":
                result = flip_horizontal(original)
                title = "Flip horizontal"
            case "vflip":
                result = flip_vertical(original)
                title = "Flip vertical"
            case "rotate":
                result = rotate_90_clockwise(original)
                title = "Rotate 90 clockwise"
            case "crop":
                top = ask_number("Top row: ")
                left = ask_number("Left column: ")
                height = ask_number("Height: ")
                width = ask_number("Width: ")
                result = crop(original, top, left, height, width)
                title = "Crop"
            case "blur":
                result = box_blur(original)
                title = "Box blur"
            case "edge":
                result = edge_detect(original)
                title = "Edge detection"
            case "exit" | "quit":
                break
            case _:
                print("Unknown command.\n")
                print_commands()
                continue

        show("BEFORE", original)
        show(f"AFTER: {title}", result)
 
if __name__ == "__main__":
    main()
