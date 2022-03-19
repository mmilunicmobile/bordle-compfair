import math
import numpy
import geopandas
import shapely.geometry
import shapely.validation
import random
from typing import Any, List, Tuple

world = geopandas.read_file("countries.geojson")
world.to_crs("+proj=cea", inplace=True)

for j, i in enumerate(world.geometry):
    if type(i) == shapely.geometry.MultiPolygon:
        polygons = geopandas.GeoSeries(i.geoms)
        index = list(polygons.area).index(max(polygons.area))
        world["geometry"][j] = polygons[index]

world = world[world.area > 144000000000]
world.reset_index(inplace=True)
del world["index"]

world["area"] = world.area


def calculate_absolute_difference(
    shape_a: geopandas.GeoSeries, shape_b: geopandas.GeoSeries
) -> float:
    area_seperate = shape_a.symmetric_difference(shape_b).area

    return area_seperate[0] / shape_b.area[0]


def calculate_score(
    shape_a: geopandas.GeoSeries, shape_b: geopandas.GeoSeries
) -> float:
    shared_area = shape_a.intersection(shape_b).area[0]

    decimal_correct = (shared_area / max(shape_a.area[0], shape_b.area[0])) ** 0.6

    distance = shape_a.centroid.distance(shape_b.centroid)[0]

    distance_decimal = (1 - distance / 40075016) ** 2

    return (decimal_correct * 2 + distance_decimal) / 3


def normalize_scale(
    shape_a: geopandas.GeoSeries, final_area: float = 1
) -> geopandas.GeoSeries:
    scales = numpy.sqrt(final_area / shape_a.area)
    return geopandas.GeoSeries(
        [
            (geopandas.GeoSeries(shape).scale(scale, scale, scale)[0])
            for shape, scale in zip(shape_a, scales)
        ]
    )


def normalize_translation(
    shape_a: geopandas.GeoSeries,
    final_position: shapely.geometry.Point = shapely.geometry.Point(0, 0),
) -> geopandas.GeoSeries:
    centers = shape_a.centroid
    return geopandas.GeoSeries(
        [
            (geopandas.GeoSeries(shape).translate(-center.x, -center.y)[0])
            for shape, center in zip(shape_a, centers)
        ]
    )


def normalize_rotation(
    shape_a: geopandas.GeoSeries, final_rotation: float = 0
) -> geopandas.GeoSeries:
    output_series = geopandas.GeoSeries()
    for i, shape in enumerate(shape_a):
        max_dist = 0
        curr_angle = 0
        xc, yc = shape.centroid.x, shape.centroid.y
        for (x, y) in shape.exterior.coords:
            dist = math.sqrt((x - xc) ** 2 + (y - yc) ** 2)
            if dist > max_dist:
                max_dist = dist
                curr_angle = math.atan2(y - yc, x - xc)
        output_series.loc[i] = geopandas.GeoSeries(shape).rotate(
            -curr_angle + final_rotation, use_radians=True
        )[0]
    return output_series


def get_geometry_coordinates(index: int):
    return [i for i in world.to_crs("+proj=wintri").loc[index].geometry.exterior.coords]


def main() -> None:
    print(
        geoseries_to_coordinates(
            coordinates_to_geoseries([(0, 0), (0, 90), (180, 0)])
            .set_crs("EPSG:4326")
            .to_crs("+proj=wintri")
        )
    )


def country_to_svg(index: int) -> None:
    with open("test.svg", "w") as f:
        f.write(world.geometry[index]._repr_svg_())


def random_country_index() -> int:
    index = random.randrange(len(world))
    return index


def get_geoseries_singular(index: int) -> geopandas.GeoSeries:
    return geopandas.GeoSeries(world.loc[index].geometry)


def geoseries_to_coordinates(geoseries: geopandas.GeoSeries) -> List[Tuple[int, int]]:
    return list(geoseries.geometry[0].exterior.coords)


def coordinates_to_geoseries(coordinates: List[Tuple[int, int]]) -> geopandas.GeoSeries:
    geometry = shapely.validation.make_valid(shapely.geometry.Polygon(coordinates))
    return geopandas.GeoSeries(geometry)


def get_country_info(index: int, info: str) -> Any:
    return world.loc[index][info]


if __name__ == "__main__":
    main()
