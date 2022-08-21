import time
from algorithms import k_means, divisive, aglomerative, aglomerative2, calc_centroid, calc_medoid
from generator import generate_points
from gui import gui, print_options, clustering_total_success, print_options_algs


def execute_alg(clustering_alg, mid_point_alg, k, all_points_array, alg_title, mid_point_title,
                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, execute_time):
    title = f"{alg_title} klastrovanie pomocou {mid_point_title}u"

    print(f"Vykonávam {title}...")
    start_time = time.process_time()

    # algoritmy [ divizivne a aglomerativne (vylepšené) ] nevyžadujú aby používateľ určil počet klastrov
    if k == -1:
        clusters, centroids_or_medoids = clustering_alg(all_points_array, MAX_SUCCESS_DISTANCE)
    else:
        clusters, centroids_or_medoids = clustering_alg(all_points_array, k, mid_point_alg)

    elapsed_time = time.process_time() - start_time
    print(f"Dĺžka vykonávania {title}: {elapsed_time}s")

    clustering_total_success(clusters, centroids_or_medoids, MAX_SUCCESS_DISTANCE, title, execute_time, elapsed_time)
    gui(clusters, centroids_or_medoids, title, mid_point_title, MIN_BORDER, MAX_BORDER, execute_time)

    return len(clusters)


def main():
    MIN_BORDER = -5000
    MAX_BORDER = 5000
    MIN_OFFSET = -100
    MAX_OFFSET = 100

    MAX_SUCCESS_DISTANCE = 500

    # zmen pocet bodov ak treba
    START_POINTS = 20
    POINTS = 20000

    while True:
        print_options()
        cmd = str(input())
        if cmd == "1":
            while True:
                try:
                    tests_count = int(input('Zadaj počet testov:\n'))
                    # k = int(input('Zadaj k pre k-means:\n'))
                    break
                except:
                    print("Musí byť číslo!")

            for i in range(tests_count):
                test_time = int(time.time())
                print(f"VYKONAVAM TESTOVACIE KOLO [{i+1}/{tests_count}]")

                # vytvori body
                all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                
                # divizivne
                k = execute_alg(divisive, calc_centroid, -1, all_points_array, "Divizivne", "centroid",
                            MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, test_time)

                # k-means centroid
                execute_alg(k_means, calc_centroid, k, all_points_array,"K-means", "centroid",
                            MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, test_time)
                # k-means medoid
                execute_alg(k_means, calc_medoid, k, all_points_array, "K-means", "medoid",
                            MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, test_time)

                # aglomerativne vylepsene
                k = execute_alg(aglomerative2, calc_centroid, -1, all_points_array, "Aglomeratívne (vylepšené)", "centroid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, test_time)

                # aglomerativne normalne
                # na zaklade vylepseneho aglomerativneho sa urci pocet klastrov
                execute_alg(aglomerative, calc_centroid, k, all_points_array, "Aglomeratívne (normálne)", "centroid",
                            MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, test_time)
        elif cmd == "2":
            while True:
                print_options_algs()
                cmd2 = str(input())
                if cmd2 == "1":
                    while True:
                        try:
                            k = int(input('Zadaj k:\n'))
                            break
                        except:
                            print("Musí byť číslo!")

                    all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                    execute_alg(k_means, calc_centroid, k, all_points_array, "K-means", "centroid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, int(time.time()))
                elif cmd2 == "2":
                    while True:
                        try:
                            k = int(input('Zadaj k:\n'))
                            break
                        except:
                            print("Musí byť číslo!")

                    all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                    execute_alg(k_means, calc_medoid, k, all_points_array, "K-means", "medoid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, int(time.time()))
                elif cmd2 == "3":
                    all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                    execute_alg(divisive, calc_centroid, -1, all_points_array, "Divizivne", "centroid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, int(time.time()))
                elif cmd2 == "4":
                    all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                    execute_alg(aglomerative2, calc_centroid, -1, all_points_array, "Aglomeratívne (vylepšené)", "centroid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, int(time.time()))
                elif cmd2 == "5":
                    while True:
                        try:
                            k = int(input('Zadaj k:\n'))
                            break
                        except:
                            print("Musí byť číslo!")

                    all_points_array = generate_points(START_POINTS, POINTS, MIN_BORDER, MAX_BORDER, MIN_OFFSET, MAX_OFFSET)
                    execute_alg(aglomerative, calc_centroid, k, all_points_array, "Aglomeratívne (normálne)", "centroid",
                                MIN_BORDER, MAX_BORDER, MAX_SUCCESS_DISTANCE, int(time.time()))
                elif cmd2 == "k":
                    break
                else:
                    print("Neznamy prikaz")

        elif cmd == "k":
            return 0
        else:
            print("Neznamy prikaz")


if __name__ == "__main__":
    main()
