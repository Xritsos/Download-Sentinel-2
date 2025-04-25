from eodag import setup_logging
from eodag import api

def onda_search(dag, start_dt, end_dt, geometry, **kwargs):
    """
    Performs product search

    Args:
        dag (EODataAccessGateway object): EODataAccessGateway should have been initialized and passed as an argument to this function
        start_dt (str): starting date
        end_dt (str): ending date
        geometry (): area of interest to search products for. For datatypes check EODataAccessGateway.search_all method

    Returns:
        search_results (eodag.api.search_result.SearchResult): list with results found from searching using ODataAPI
    """
    setup_logging(verbose=2)
    search_results = dag.search_all(
        geom=geometry, start=start_dt, end=end_dt, provider="cop_dataspace", **kwargs
    )

    return search_results


# TODO: The name of the function should change
def get_start_time(search_results, attrname="startTimeFromAscendingNode"):
    """
    Returns a list of value for the given key (attrname) of the search results properties

    Args:
        search_results (eodag.api.search_result.SearchResult object): list of products
    Returns:
        start_time (list): list of strings of sensing (start) time for each product
    """
    start_time = [item.properties[attrname] for item in search_results]
    return start_time


def get_sorted_results(search_results):
    """
    Args:
        search_results (eodag.api.search_result.SearchResult object): list of products
    Returns:
        eodag.api.search_result.SearchResult object sorted based on sensing date
    """
    # get startTime (sensing) list
    startTime = get_start_time(
        search_results, attrname="startTimeFromAscendingNode"
    )
    # sort search results
    search_results = [res for _, res in sorted(zip(startTime, search_results))]

    return api.search_result.SearchResult(search_results)

