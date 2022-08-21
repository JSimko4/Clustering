import math
import random

################################################################################
#                                   DISTANCE                                   #
################################################################################


def euclidean_distance(point1, point2):
    return math.sqrt(math.pow(point1[0]-point2[0], 2) + math.pow(point1[1]-point2[1], 2))


################################################################################
#                                   SUCCESS                                    #
################################################################################


def get_success(cluster, centroid_or_medoid):
    average_distance_from_center = 0.0
    for point in cluster:
        distance_from_center = euclidean_distance(point, centroid_or_medoid)
        average_distance_from_center += distance_from_center

    return average_distance_from_center / len(cluster)


################################################################################
#                               CENTROID/MEDOID                                #
################################################################################


def calc_centroid(cluster):
    total_x = total_y = 0
    points_count = len(cluster)
    for point in cluster:
        total_x += point[0]
        total_y += point[1]

    return int(total_x/points_count), int(total_y/points_count)


def calc_medoid(cluster):
    medoid = None
    min_distance = math.inf

    points_count = len(cluster)
    for i in range(points_count):
        candidate_total_distance = 0

        for j in range(points_count):
            if i == j:  # vzdialenost sam do seba program nezaujima
                continue

            candidate_total_distance += euclidean_distance(cluster[i], cluster[j])
            if candidate_total_distance >= min_distance:
                break

        if min_distance > candidate_total_distance:
            min_distance = candidate_total_distance
            medoid = cluster[i]

    return medoid

# medoid vylepseny -  nakoniec som ho nepouzil kvoli pamatovej narocnosti
# def calc_medoid(cluster):
#     medoid = None
#     min_distance = math.inf
#
#     distances = {}
#     points_count = len(cluster)
#     for i in range(points_count):
#         candidate_total_distance = 0
#         for j in range(points_count):
#             if i == j:  # vzdialenost sam do seba program nezaujima
#                 continue
#
#             if ((cluster[i]), cluster[j]) in distances:
#                 candidate_total_distance += distances[(cluster[i]), cluster[j]]
#             else:
#                 distance = euclidean_distance(cluster[i], cluster[j])
#                 distances[((cluster[j]), cluster[i])] = distance
#                 candidate_total_distance += distance
#
#             if candidate_total_distance >= min_distance:
#                 break
#
#         if min_distance > candidate_total_distance:
#             min_distance = candidate_total_distance
#             medoid = cluster[i]
#
#     return medoid


################################################################################
#                                  K-MEANS                                     #
################################################################################


def assign_to_clusters(all_points, centroids_or_medoids, k):
    clusters = [[] for i in range(0, k)]

    # pre kazdy z bodov vypocitam vzdialenost do centroidu/medoidu vsetkych klastrov
    for point in all_points:
        min_distance = (math.inf, 0)

        for cluster_index in range(0, k):
            distance = (euclidean_distance(point, centroids_or_medoids[cluster_index]), cluster_index)

            if min_distance[0] > distance[0]:
                min_distance = distance

        clusters[min_distance[1]].append(point)

    return clusters


def k_means_initial(all_points_array, k):
    initial_points = {}

    picked_unique = 0
    while picked_unique != k:
        picked_point = random.choice(all_points_array)
        x, y = picked_point[0], picked_point[1]

        if (x, y) not in initial_points.values():
            initial_points[(x, y)] = (x, y)
            picked_unique += 1

    return list(initial_points)


def k_means(all_points, k, calc_centroid_or_medoid_function):
    # navratove polia algoritmu/funkcie
    clusters = []
    centroids_or_medoids = [(0, 0) for i in range(0, k)]

    # 1. - initial (pick k random points)
    initial_points = k_means_initial(all_points, k)
    for i in range(0, k):
        centroids_or_medoids[i] = initial_points[i]

    not_changed_centroids_or_medoids = 0
    while not_changed_centroids_or_medoids < k:
        # priradi jednotlive body do klastrov
        clusters = assign_to_clusters(all_points, centroids_or_medoids, k)

        # prepocita centroid/medoid pre kazdy z klastrov
        for i in range(0, k):
            last_centroids_or_medoids = centroids_or_medoids[:]

            if clusters[i]:
                centroids_or_medoids[i] = calc_centroid_or_medoid_function(clusters[i])

            # ak su centroidy/medoidy rovnake tym z minulej iteracie tak k-means konci
            if last_centroids_or_medoids[i] == centroids_or_medoids[i]:
                not_changed_centroids_or_medoids += 1
            else:
                not_changed_centroids_or_medoids = 0

    return clusters, centroids_or_medoids


################################################################################
#                                 DIVISIVE                                     #
################################################################################

# Rozdeluj klaster pomocou k-means dokedy centroid neni pod 500
def divisive(all_points, MAX_SUCCESS_DISTANCE):
    # navratove polia algoritmu/funkcie
    result_clusters = []
    result_centroids = []

    # rozdeli 1 velky klaster na 2
    clusters, centroids = k_means(all_points, 2, calc_centroid)

    # rozdeľuje klastre na menšie dokedy nemaju vsetky priemernu vzdialenost mensiu ako 500
    while clusters:
        clusters_count = len(clusters)

        for cluster_index in range(0, clusters_count):
            # klaster uz nebude rozdeleny pretoze splna podmienku uspesnosti
            if get_success(clusters[cluster_index], centroids[cluster_index]) < MAX_SUCCESS_DISTANCE:
                result_clusters.append(clusters[cluster_index])
                result_centroids.append(centroids[cluster_index])
            else:  # klaster bude rozdeleny na 2 mensie
                clusters_split, centroids_split = k_means(clusters[cluster_index], 2, calc_centroid)
                clusters.extend(clusters_split)
                centroids.extend(centroids_split)

        clusters = clusters[clusters_count:]
        centroids = centroids[clusters_count:]

    return result_clusters, result_centroids


################################################################################
#                                  AGLOMERATIVE                                #
################################################################################

def find_smallest_distance_indexes(distance_matrix, n):
    smallest = (float(math.inf), 0, 0)

    for i in range(0, n):
        for j in range(i+1, n):
            distance = distance_matrix[i][j]

            if smallest[0] > distance:
                smallest = (distance, i, j)

    return smallest

# normalne aglomerativne
def aglomerative(all_points, k, calc_centroid_or_medoid_function):
    # navratove polia algoritmu/funkcie
    result_clusters = []
    result_centroids = []

    # vytvor maticu vzdialenosti a vytvor kazdemu bodu vlastny klaster
    distance_matrix = []
    all_points_count = len(all_points)
    for i in range(0, all_points_count):
        distance_matrix.append([])

        result_clusters.append([all_points[i]])
        result_centroids.append(all_points[i])
        for j in range(0, all_points_count):
            distance = 0
            if i != j:
                distance = euclidean_distance(all_points[i], all_points[j])

            distance_matrix[i].append(distance)

    clusters_count = all_points_count
    while clusters_count != k:
        len_distance_matrix = len(distance_matrix)
        smallest_merge_distance, smallest1, smallest2 = find_smallest_distance_indexes(distance_matrix, len_distance_matrix)

        # merge
        result_clusters[smallest1].extend(result_clusters[smallest2])

        # aktualizuj centroid
        updated_centroid_x, updated_centroid_y = calc_centroid_or_medoid_function(result_clusters[smallest1])
        result_centroids[smallest1] = (updated_centroid_x, updated_centroid_y)

        # aktualizuje hodnoty matice pre riadok a stlpec ktory ostava
        for i in range(0, len_distance_matrix):
            distance_matrix[smallest1][i] = euclidean_distance(result_centroids[smallest1], result_centroids[i])
            distance_matrix[i][smallest1] = distance_matrix[smallest1][i]

        # vymaze stlpec z kazdeho riadka
        for i in range(0, len(distance_matrix)):
            del distance_matrix[i][smallest2]

        # vymaze riadok
        del distance_matrix[smallest2]

        # vymaze povodny klaster ktory sa spojil s druhym (aj jeho centroid)
        del result_clusters[smallest2]
        del result_centroids[smallest2]

        clusters_count -= 1

    return result_clusters, result_centroids

# vylepsene aglomerativne
def aglomerative2(all_points, MAX_SUCCESS_DISTANCE):
    # navratove polia algoritmu/funkcie
    clusters = []
    centroids = []
    result_clusters = []
    result_centroids = []

    # vytvor maticu vzdialenosti a vytvor kazdemu bodu vlastny klaster
    distance_matrix = []
    all_points_count = len(all_points)
    for i in range(0, all_points_count):
        distance_matrix.append([])

        clusters.append([all_points[i]])
        centroids.append(all_points[i])
        for j in range(0, all_points_count):
            distance = 0
            if i != j:
                distance = euclidean_distance(all_points[i], all_points[j])

            distance_matrix[i].append(distance)

    clusters_count = len(clusters)
    while clusters:
        # ak by ostal na rozdelenie len 1 samostatny klaster (posledny) tak sa uz nema s kym spojit
        # - prida sa do riesenia a koniec cyklu
        if clusters_count == 1:
            last_cluster = clusters[0]
            last_cluster_centroid = calc_centroid(last_cluster)
            # tmp_centroid = (x, y)
            result_clusters.append(last_cluster)
            result_centroids.append(last_cluster_centroid)
            break

        len_distance_matrix = len(distance_matrix)
        smallest_merge_distance, smallest1, smallest2 = find_smallest_distance_indexes(distance_matrix, len_distance_matrix)

        # merge
        tmp = clusters[smallest1].copy()
        clusters[smallest1].extend(clusters[smallest2])

        # aktualizuj centroid
        updated_centroid_x, updated_centroid_y = calc_centroid(clusters[smallest1])
        centroids[smallest1] = (updated_centroid_x, updated_centroid_y)

        if get_success(clusters[smallest1], centroids[smallest1]) > MAX_SUCCESS_DISTANCE:
            # prida do vysledku obidva klastre
            result_clusters.append(tmp)
            # x, y = calc_centroid(tmp)
            tmp_centroid = calc_centroid(tmp) # (x, y)
            result_centroids.append(tmp_centroid)

            result_clusters.append(clusters[smallest2])
            result_centroids.append(centroids[smallest2])

            # vymaze stlpce pre tieto klastre
            for i in range(0, len_distance_matrix):
                if smallest1 > smallest2:
                    del distance_matrix[i][smallest1]
                    del distance_matrix[i][smallest2]
                else:
                    del distance_matrix[i][smallest2]
                    del distance_matrix[i][smallest1]

            # vymaze klastre, centroidy
            # a riadky z matice vzdialenosti
            if smallest1 > smallest2:
                del clusters[smallest1]
                del centroids[smallest1]
                del clusters[smallest2]
                del centroids[smallest2]

                del distance_matrix[smallest1]
                del distance_matrix[smallest2]
            else:
                del clusters[smallest2]
                del centroids[smallest2]
                del clusters[smallest1]
                del centroids[smallest1]

                del distance_matrix[smallest2]
                del distance_matrix[smallest1]
            clusters_count -= 2
        else:
            # aktualizuje hodnoty matice pre riadok ktory ostava
            for i in range(0, len_distance_matrix):
                distance_matrix[smallest1][i] = euclidean_distance(centroids[smallest1], centroids[i])
                distance_matrix[i][smallest1] = distance_matrix[smallest1][i]

            # vymaze stlpec z kazdeho riadka
            for i in range(0, len(distance_matrix)):
                del distance_matrix[i][smallest2]

            # vymaze riadok
            del distance_matrix[smallest2]

            # vymaze povodny klaster ktory sa spojil s druhym (aj jeho centroid)
            del clusters[smallest2]
            del centroids[smallest2]

            clusters_count -= 1

    return result_clusters, result_centroids
