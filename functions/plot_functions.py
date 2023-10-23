# import libraries
from PIL import Image
import urllib.request


class BboxLocator:
    """
    A helper class to locate a bbox in a given axes.
    Will be used in our leaderboards.
    """

    def __init__(self, bbox, transform):
        self._bbox = bbox
        self._transform = transform

    def __call__(self, ax, renderer):
        _bbox = self._transform.transform_bbox(self._bbox)
        return ax.figure.transFigure.inverted().transform_bbox(_bbox)


def draw_table_image(img_url, ax):
    """
    Draws table image
    """
    club_icon = Image.open(urllib.request.urlopen(img_url))
    club_icon.resize((100, 100))
    ax.imshow(club_icon)
    ax.axis("off")
    return ax
