import random
import time


def generate_start_points(n_start, MIN_BORDER, MAX_BORDER):
    print(f"Generujem začiatočných {n_start} bodov!")

    start_points = {}
    for i in range(n_start):
        found_unique = False

        while not found_unique:
            x = random.randint(MIN_BORDER, MAX_BORDER)
            y = random.randint(MIN_BORDER, MAX_BORDER)

            if (x, y) not in start_points.values():
                start_points[(x, y)] = (x, y)
                found_unique = True

    return start_points


def get_offsetted_coordinate(coordinate, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET):
    if coordinate + MAX_OFFSET > MAX_BORDER:
        new_max_offset = MAX_BORDER - coordinate
        offset = random.randint(MIN_OFFSET, new_max_offset)
    elif coordinate + MIN_OFFSET < MIN_BORDER:
        new_min_offset = MIN_BORDER - coordinate
        offset = random.randint(new_min_offset, MAX_OFFSET)
    else:
        offset = random.randint(MIN_OFFSET, MAX_OFFSET)

    return coordinate + offset


def generate_aditional_points(start_points, n_add, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET):
    print(f"Generujem ďalších {n_add} bodov!")

    all_points = {}
    all_points.update(start_points)
    all_points_array = list(all_points.values())
    for i in range(n_add):
        picked_point = random.choice(all_points_array)

        found_unique = False
        while not found_unique:
            x = get_offsetted_coordinate(picked_point[0], MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
            y = get_offsetted_coordinate(picked_point[1], MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)

            if (x, y) not in all_points.values():
                all_points[(x, y)] = (x, y)
                all_points_array.append((x, y))
                found_unique = True

    return all_points


def generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET):
    print(f"Začínam generovať body...")
    start_time = time.process_time()
    start_points_created = generate_start_points(START_POINTS, MIN_BORDER, MAX_BORDER)
    all_points = generate_aditional_points(start_points_created, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
    elapsed_time = time.process_time() - start_time
    print(f"Dĺžka generovania všetkých bodov: {elapsed_time}s")

    return list(all_points)