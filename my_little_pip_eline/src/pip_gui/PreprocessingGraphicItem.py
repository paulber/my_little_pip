
from src.pip_gui.PipelineGraphicItem import *


class PreprocessingGraphicItem(PipelineGraphicItem):

    def __init__(self, text="?", input_number=0, output=0, *args, **kwargs):
        super().__init__(text, input_number, output, QColor(31, 176, 224), *args, **kwargs)
