import numpy as np
import matplotlib.pyplot as plt
import rasterio
import matplotlib.colors as colors
import os
from PIL import Image
import multiprocessing
import functions
from natsort import natsorted
import geopandas as gpd
from rasterio.plot import show
from rasterio.features import rasterize

#Dependencias para que funcione la instalación de rasterio en el .exe
import rasterio.control
import rasterio.crs
import rasterio.sample
import rasterio.vrt
import rasterio._features
import fiona
import fiona.schema
import sys

## Local function definition
def shapefile_rasterize(vector_file, raster_file, id_field):
    """
        Rasterizes the vector file based on the reference raster file. It requires the name of the field containing
        the ID(which needs to be numeric).

        Parameters
        ----------
        vector_file : str
            File path to the vector file (.shp).
        raster_file : str
            File path to the reference raster file (.tif).
        id_field : str
            Name of the field containing the ID (should be numeric).

        Returns
        -------
        numpy.ndarray
            Rasterized array representing the vector file based on the reference raster.

        """

    # Open the vector file using GeoPandas
    gdf = gpd.read_file(vector_file)

    # Open the reference raster file with rasterio to obtain geospatial information
    with rasterio.open(raster_file) as src:
        profile = src.profile

        # Create an array of zeros with the same dimensions as the reference raster
        rasterize_array = np.zeros((src.height, src.width), dtype=np.float32)

        # Rasterize the vector file using the ID field values
        for id_value in gdf[id_field]:
            shapes = ((geom, value) for geom, value in zip(gdf.geometry, gdf[id_field]))
            burned = rasterize(shapes, out=rasterize_array, fill=0, transform=src.transform)

    return rasterize_array

def processing_id(ids):
    """
        Defines the processing_id function, calculating the growing algorithm for each ID.

        Parameters
        ----------
        ids : list
            List of IDs for which the growing function needs to be computed.

        Returns
        -------
        None
            This function does not return any value; it performs operations to calculate scenario zero for each ID and
            saves the results as GeoTIFF files.

        """
    for id in ids:
        # Execute the algorithm
        escenario_0 = functions.escenario_cero(zNucleo, dRue, id=id, size=size, threshold=threshold)

        # Save the final result in a GeoTIFF layer using the original input 'rn2000_rast' as a template
        with rasterio.open(raster_file) as rst:
            profile = rst.profile

        with rasterio.open(directory + '/' + str(id) + '.tif', 'w', **profile) as new_rst:
            new_rst.write(escenario_0, 1)  # If space becomes an issue (new_rst.write(escenario_0.astype(rasterio.uint8), 1)

    return None


def get_escenario_cero(zNucleo, dRue, size, threshold, directory):
    """
    Computes the growing algorith for all the seeds provided in zNucleo using multiprocessing.

    Parameters
    ----------
    zNucleo : numpy.ndarray
        Array corresponding to the seed map.
    dRue : numpy.ndarray
        Array containing land condition information.
    size : int
        Size parameter for the calculation.
    threshold : int
        Threshold parameter used in the calculation.
    directory : str
        Directory path for storing the computed results.

    Returns
    -------
    None
        This function does not return any value; it performs operations to compute and save scenario zero results.

    Notes
    -----
    - This function divides the IDs into subsets and computes the scenario zero using multiprocessing.
    - It opens and overlays all the images, saves the final result as a GeoTIFF file, and generates an image of the result.

    The function first selects all IDs from zNucleo (excluding the background), then divides the IDs and calculates
    them using multiprocessing. It then opens all images, overlays them, and saves the final result as a GeoTIFF file
    named 'resultado.tif'. Additionally, it generates an image 'resultado.png' that visualizes the computed scenario
    zero along with land condition information and vector boundary contours.
    """

    # Select all the IDs from zNucleo (excluding the background)
    ids = list(np.unique(zNucleo).astype('int'))
    ids.remove(0)  # Zero represents the background

    # Divide the IDs and perform multiprocessing
    if __name__ == '__main__':

        # Divide the list of IDs into multiple subsets
        num_procesos = multiprocessing.cpu_count()
        chunks = [[] for _ in range(num_procesos)]
        for i, id in enumerate(ids):
            chunks[i % num_procesos].append(id)

        # Execute the function in parallel
        with multiprocessing.Pool(processes=num_procesos) as pool:
            result = pool.map_async(processing_id, chunks)
            result.wait()

            # Open all images and overlay them
            resultado = np.zeros_like(zNucleo)
            for file in natsorted(os.listdir(directory)):
                if file.endswith(".tif"):
                    if not file.startswith('resultado'):
                        x = np.asarray(Image.open(os.path.join(directory, file)))
                    resultado += x

            # Save the final result as a GeoTIFF file
            with rasterio.open(raster_file) as rst:
                profile = rst.profile

            with rasterio.open(directory + '/resultado.tif', 'w', **profile) as new_rst:
                new_rst.write(resultado,1)

            # Save an image of the result
            colors_hot_list = ['#FBB4AE', '#660000', '#981800', '#cc4c00', '#ff8000', '#ffb232', '#ffe666', '#ffffc5', '#fffff5'] #Cambiar legenda
            cmap_hot = colors.ListedColormap(colors_hot_list)

            # Auxiliar mask for visualization
            dRue_mask = dRue > 0
            dRue_mask = np.where(dRue_mask, dRue_mask, np.nan)

            src = rasterio.open(directory + '/resultado.tif')
            vectorial = gpd.read_file(vector_file)
            contorno = vectorial.boundary

            # Create the figure
            fig, ax = plt.subplots()
            extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
            aux_mask = src.read()[0]
            aux_mask[dRue == 0] = np.nan
            image_hidden = ax.imshow(aux_mask, extent=extent, cmap = cmap_hot, vmin = 0, vmax = 8)
            fig.colorbar(image_hidden, ax=ax)
            extent=[src.bounds[0], src.bounds[2], src.bounds[1], src.bounds[3]]
            ax = rasterio.plot.show(dRue_mask, extent=extent, ax=ax, cmap = 'Pastel1')
            rasterio.plot.show(src, ax=ax, cmap = cmap_hot , vmin = 0, vmax = 8)
            plt.rcParams['hatch.linewidth'] = 0.1
            contorno.plot(ax = ax, color = 'white', linewidth=0.1)
            plt.axis('off')
            plt.savefig(directory + '/resultado.png', dpi = 1500.0)

    return None

##
# Abrimos las imagenes TIFF
# Solicita al usuario que ingrese los path
# vector_file = input("Ingrese el path al archivo vectorial: ")
# id_field = input("Ingrese el campo de ID (debe ser un campo numerico) asociado al archivo vectorial: ")
# raster_file = input("Ingrese el path al archivo raster: ")
#
# # Definimos los parámetros de la ejecución
# size = int(input("Ingrese el tamaño de kernel para la ejcucion: "))
# threshold = float(input("Ingrese el umbral de Orloci para la ejcucion: "))

import json

# Cargar los parámetros desde el archivo JSON
with open("config.json", "r") as json_file:
    parameters = json.load(json_file)

# Acceder a los parámetros
vector_file = parameters["vector_file"]
raster_file = parameters["raster_file"]
id_field = parameters["id_field"]
size = parameters["size"]
threshold = parameters["threshold"]


# Abrimos los ficheros
zNucleo = shapefile_rasterize(vector_file, raster_file, id_field)
with rasterio.open(raster_file, 'r') as rst:
    dRue = rst.read(1)


# Definimos el lugar donde se van a guardar las imagenes
directory = 'output/' + 'size (' + str(size) + ') - threshold (' + str(threshold) +')'
if not os.path.exists(directory):
    os.makedirs(directory)

# Ejecutamos el algoritmo
get_escenario_cero(zNucleo, dRue, size, threshold, directory)

##

