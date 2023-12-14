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


## Multiprocessing functions definition
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
    # Create dir to save the tiff files
    if not os.path.exists(directory + '/ImagesTIFF'):
        os.makedirs(directory + '/ImagesTIFF')

    for id in ids:
        # Execute the algorithm
        escenario_0 = functions.escenario_cero(zNucleo, dRue, id=id, size=size, threshold=threshold)

        # Save final image as .png
        functions.save_image(zNucleo, dRue, growingLIC=escenario_0, id=id, dir=directory)

        # Save the final result in a GeoTIFF layer using the original input as a template
        with rasterio.open(raster_file) as rst:
            profile = rst.profile

        with rasterio.open(directory + '/ImagesTIFF' + '/' + str(id) + '.tif', 'w', **profile) as new_rst:
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
            for file in natsorted(os.listdir(directory + '/ImagesTIFF')):
                if file.endswith(".tif"):
                    if not file.startswith('resultado'):
                        x = np.asarray(Image.open(os.path.join(directory + '/ImagesTIFF', file)))
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

## Run the growing algorithm
# Define parameters
vector_file = "inputs/LIC_Seeds.shp"
raster_file = "inputs/2dRue.tif"
id_field = "OBJECTID"
size = 3
threshold = 0.57317317

# Open files
zNucleo = functions.shapefile_rasterize(vector_file, raster_file, id_field)
with rasterio.open(raster_file, 'r') as rst:
    dRue = rst.read(1)

# Create directory to save the outputs
directory = 'outputs/' + 'size (' + str(size) + ') - threshold (' + str(threshold) +')'
if not os.path.exists(directory):
    os.makedirs(directory)

# Execute the algorithm
get_escenario_cero(zNucleo, dRue, size, threshold, directory)


