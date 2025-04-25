from datetime import datetime
import yaml
from shapely.geometry import shape
from eodag import EODataAccessGateway
from eodag import setup_logging

import downutils
import discoverutils
import utils

def main():
    ############################ Change parameters ################################
    ###############################################################################
    SATELLITE = "Sentinel-2-L2A" # available satellites in satellite_list.yml

    # date of interest
    END_DATE = "2021-12-19"

    # Polygon of AOI (as copied from Copernicus Browser)
    POLYGON = {"type":"Polygon","coordinates":[[[21.84185,40.245729],[21.84185,40.295763],[21.932831,40.295763],[21.932831,40.245729],[21.84185,40.245729]]]}
    WKT_F = shape(POLYGON)

    # Where to download products
    DATA_PATH = "./sentinel-2/"

    # Copernicus credentials
    COP_USERNAME = "your_username"
    COP_PASSWORD = "your_password"
    ###############################################################################

    # Satellite name checker
    with open("./satellite_list.yml", "r") as f:
        sats = yaml.safe_load(f)

    if SATELLITE not in sats.keys():
        raise ValueError(
            f'List of allowed satellites are: {", ".join(sats.keys())}. Please retry.'
        )

    product_type = sats[SATELLITE]

    dag = EODataAccessGateway()
    setup_logging(verbose=3)

    with open("./eodag_ref.yml", 'r') as f:
        my_yml = yaml.safe_load(f)

    my_yml["cop_dataspace"]["download"]["output_dir"] = DATA_PATH
    my_yml["cop_dataspace"]["auth"]["credentials"]["username"] = COP_USERNAME
    my_yml["cop_dataspace"]["auth"]["credentials"]["password"] = COP_PASSWORD

    config_yaml = yaml.dump(my_yml)

    dag.update_providers_config(config_yaml)
    dag.set_preferred_provider("cop_dataspace")

    end_dt = datetime.strptime(END_DATE, "%Y-%m-%d").replace(
        hour=23, minute=59, second=59, microsecond=999999
    )

    start_dt = end_dt.replace(hour=0, minute=0, second=0, microsecond=0)

    k = 0
    while True:
        k += 1

        # Set data search arguments
        kwargs = {
            "start_dt": utils.dt_to_longstr(start_dt),
            "end_dt": utils.dt_to_longstr(end_dt),
            "geometry": WKT_F,
            "productType": product_type,
        }
        # Perform searchs
        try:
            search_results = downutils.onda_search(dag, **kwargs)
        except Exception as ex:
            print(f"failed to search: {ex}")

        if len(set(search_results)) == len(search_results):
            print(f"Products were searched {k} time(s)")
            break

        if k == 10:
            raise RecursionError(
                f"Products were searched {k} times. Every time the products returned were problematic. Please retry or contact data provider support."
            )

    if len(search_results) >= 2:
        # Check if they have common sensing date
        sensing_dates = downutils.get_start_time(
            search_results
        )  # Get sensing dates of products

        if len(set(sensing_dates)) == 1:
            print(
                f"The Sentinel-2 products that were discovered have {sensing_dates[0]} as a common sensing date. Proceeding with further filtering.",
            )

            # Check if there is product that completely covers the AOI
            if discoverutils.products_within_aoi(search_results, WKT_F):
                # search_results = discoverutils.products_within_aoi(search_results, wkt_f)[:1] # Choose one product (it doesn't matter which one)
                search_results = discoverutils.products_within_aoi(
                    search_results, WKT_F
                )
            else:
                print(
                    "All Sentinel-2 products that were discovered do not fully cover the AOI. Proceeding with further filtering."
                )

        elif len(set(sensing_dates)) >= 2:
            print(
                "The Sentinel-2 products that were discovered have different sensing dates. Something was wrong with searching. Exiting with error code 0."
            )


    product_paths = dag.download_all(search_results, wait=20, timeout=380)

    print()
    print(f"SAFE downloaded in: {product_paths}")

if __name__ == "__main__":
    
    main()
    