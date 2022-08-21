import os
from matplotlib import pyplot as plt
from algorithms import get_success


def gui(clusters, centroids_or_medoids, title_method, mid_point, MIN_BORDER, MAX_BORDER, test_time):
    print("Vytváram vizualizáciu...\n")

    plt.style.use("seaborn")
    plt.figure(dpi=300)
    plt.title(title_method)
    plt.xlabel('OS X')
    plt.ylabel('OS Y')

    ax = plt.gca()
    ax.set_xlim([MIN_BORDER-100, MAX_BORDER+100])
    ax.set_ylim([MIN_BORDER-100, MAX_BORDER+100])

    # 30 farieb
    colors = ['#e6194b', '#3cb44b', "#00615f", '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6',
              '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000',
              '#614931', '#000075', '#808080', '#9ACD32', '#7B68EE', '#FF7F50', '#BC8F8F', '#B8860B', '#4169E1',
              '#8A2BE2', '#B22222', '#FFA500']

    x_points = []
    y_points = []
    for i in range(len(clusters)):
        for point in clusters[i]:
            x_points.append(point[0])
            y_points.append(point[1])

        plt.scatter(x_points, y_points, s=13, c=colors[i], edgecolor="black", linewidth=0.2, alpha=0.6)
        x_points.clear()
        y_points.clear()

    first = True
    for i in range(len(centroids_or_medoids)):
        if len(clusters[i]) > 0:
            if first:
                plt.scatter(centroids_or_medoids[i][0], centroids_or_medoids[i][1], s=50, c=colors[i], edgecolor="black", linewidth=1, marker="X", label=mid_point)
                first = False
            else:
                plt.scatter(centroids_or_medoids[i][0], centroids_or_medoids[i][1], s=50, c=colors[i], edgecolor="black", linewidth=1, marker="X")

            plt.annotate(i, (centroids_or_medoids[i][0], centroids_or_medoids[i][1]), color="white", ha='center', va="center", fontsize=3)

    # vytvori priecinky aby sa dal graf ulozit
    if not os.path.exists("GRAFY"):
        os.makedirs("GRAFY")

    if not os.path.exists(f"GRAFY/EXECUTED_TEST{test_time}"):
        os.makedirs(f"GRAFY/EXECUTED_TEST{test_time}")

    ax.legend(shadow=True, fontsize='x-small')
    legend = plt.legend(title='Legenda', frameon=1, facecolor='darkgrey', labelcolor='w')
    plt.setp(legend.get_title(), color='w')

    plt.savefig(f"GRAFY/EXECUTED_TEST{test_time}/{title_method}.jpg")
    plt.show()  # --> moze odkomentovat ak chce graf rovno zobrazit
    print(f"Vizualizácia a úspešnosť klastrovania sa uložili do GRAFY/EXECUTED_TEST{test_time}/\n")
    plt.close()


def clustering_total_success(clusters, centroids_or_medoids, MAX_SUCCESS_DISTANCE, title, test_time, elapsed_time):
    if not os.path.exists("GRAFY"):
        os.makedirs("GRAFY")

    if not os.path.exists(f"GRAFY/EXECUTED_TEST{test_time}"):
        os.makedirs(f"GRAFY/EXECUTED_TEST{test_time}")

    file = open(f"GRAFY/EXECUTED_TEST{test_time}/{title}.txt", 'w')
    file.write(f"Dlzka vykonavania {title}: {elapsed_time}s\n\n")

    total = len(clusters)
    success = 0
    for cluster_index in range(0, len(clusters)):
        # osetrenie - pri k-means moze nastat existencia prazdneho klastra (ak bolo zvolene nespravne k)
        if len(clusters[cluster_index]) == 0:
            total -= 1
            continue

        # ak je priemerna vzdialenost od stredu vacsia ako MAX_SUCCESS_DISTANCE tak zhlukovac je neuspesny
        average_distance_from_center = get_success(clusters[cluster_index], centroids_or_medoids[cluster_index])
        if average_distance_from_center > MAX_SUCCESS_DISTANCE:
            file.write(f"Priemerna vzdialenost klastra c. {cluster_index}: {average_distance_from_center}"
                       f"\nUspesnost = 0%\n")
        else:
            file.write(f"Priemerna vzdialenost klastra c. {cluster_index}: {average_distance_from_center}"
                       f"\nUspesnost = 100%\n")
            success += 1

    file.write(f"\nUSPESNOST: {success}/{total}")
    file.close()

def print_options():
    print("1\t : \t Testovanie vsetkych algoritmov - vykona testovanie vyuzite a vysvetlene v dokumentacii.")
    print("2\t : \t Testovanie jedneho vybraneho algoritmu")
    print("k\t : \t ukonci program")

def print_options_algs():
    print("1\t : \t K-means - centroid")
    print("2\t : \t K-means - medoid")
    print("3\t : \t Divizivne - centroid")
    print("4\t : \t Aglomerativne (vylepsene) - centroid")
    print("5\t : \t Aglomerativne (obycajne) - centroid")
    print("k\t : \t vratit sa späť")
