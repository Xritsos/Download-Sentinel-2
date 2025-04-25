from collections import Counter

from eodag import api
from shapely import wkt


def products_within_aoi(search_results, wkt_f):
    """
    Args:
        search_results (eodag.api.search_result.SearchResult instance): list of products
        wkt_f (str): the given AOI as a WKT polygon
    Returns:
        filtered_results (eodag.api.search_result.SearchResult instance): list of selected products
    """
    wkt_f = wkt.loads(wkt_f)  # convert to shapely.geometry

    # added functionality to keep only latest processed products
    for product in search_results:
        # the processing id is the Nxxxx in the naming template
        try:
            processing_id = int(product.as_dict()["id"].split("_")[3][2])

            if processing_id != 5:
                search_results.remove(product)
        except Exception as ex:
            print()
            print(f"Failed to filter based on processing id due to: {ex}")

    # Keep products
    filtered_results = api.search_result.SearchResult(
        [
            product
            for product in search_results
            if wkt_f.within(product.geometry)
        ]
    )

    return filtered_results


def get_orbits(search_results):
    """
    Args:
        search_results (eodag.api.search_result.SearchResult)

    Returns:
        relative_orbits (list): list of integers or strings
    """
    rel_orb = list(
        [
            int(product.properties["relativeOrbitNumber"])
            for product in search_results
        ]
    )

    n_relative_orbits = list(Counter(rel_orb).values())
    relative_orbits = list(Counter(rel_orb).keys())

    return n_relative_orbits, relative_orbits
