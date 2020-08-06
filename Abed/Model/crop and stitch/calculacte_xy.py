def calcul_xyz_array(img_x, img_y, tile_x, tile_y, cross_x, cross_y):
    array = []

    modu_x = cross_x
    modu_y = cross_y
    current_x = 0
    current_y = 0

    while current_y + tile_y <= img_y:

        while current_x + tile_x <= img_x:

            array.append((current_x, current_y))

            if current_x + tile_x == img_x:
                break

            current_x += tile_x

            if current_x + tile_x > img_x:  # we reached end of x

                array.append((img_x - tile_x, current_y))
                break
            if current_x == tile_x:
                current_x += - modu_x

        current_x = 0   # new line
        if current_y + tile_y == img_y:
            break

        current_y += tile_y

        if current_y + tile_y > img_y:  # we reached end of y

            current_y = img_y - tile_y
            continue

        if current_y == tile_y:
            current_y += - modu_y

    return array


def calcul_xy_array(img_x, img_y, tile_x, tile_y):
    array = []

    modu_x = img_x % tile_x
    modu_y = img_y % tile_y
    div_x = img_x // tile_x
    div_y = img_y // tile_y
    current_x = 0
    current_y = 0

    for i in range(div_y):
        for j in range(div_x):
            array.append((current_x, current_y))
            current_x += tile_x
        if modu_x:
            array.append((img_x - tile_x, current_y))
        current_y += tile_y
        current_x = 0

    if modu_y:
        current_y = img_y - tile_y
        for j in range(div_x):
            array.append((current_x, current_y))
            current_x += tile_x
        if modu_x:
            array.append((img_x - tile_x, current_y))

    return array

# print(calcul_xy_array(1024,768,200,200))
# print(calcul_xyz_array(1024,768,200,200,0,0))
