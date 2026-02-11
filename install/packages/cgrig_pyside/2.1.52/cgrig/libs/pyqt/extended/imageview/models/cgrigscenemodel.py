# -*- coding: utf-8 -*-
import os

from cgrig.libs.pyqt.extended.imageview.model import MiniBrowserFileModel
from cgrig.libs.cgrigscene import cgrigscenefiles
from cgrig.libs.cgrigscene.constants import CGRIGSCENE_EXT


class CgRigSceneModel(MiniBrowserFileModel):
    def __init__(self, view, directories=None, chunkCount=0, uniformIcons=False,
                 assetPreference=None, extensions=None):
        """Loads .cgrigscene model data from a directory for a ThumbnailView widget

        Pulls thumbnails which are in dependency directories and tooltips are generated from the file.cgrigInfo files.

        Also see the inherited class FileModel() in cgrig_pyside for more functionality and documentation.:
            cgrig.libs.pyqt.extended.imageview.model.FileModel()

        This class can be overridden further for custom image loading in subdirectories such as Skydomes or Controls \
        which use the .cgrigScene tag and thumbnail information.

        :param view: The viewer to assign this model data?
        :type view: qtWidget?
        :param directories: The directory full path where the .cgrigScenes live
        :type directories: list[str] or list[DirectoryPath]
        :param chunkCount: The number of images to load at a time into the ThumbnailView widget
        :type chunkCount: int
        """
        extensions = extensions or [CGRIGSCENE_EXT]
        super(CgRigSceneModel, self).__init__(view, extensions=extensions,
                                            directories=directories, chunkCount=chunkCount,
                                            uniformIcons=uniformIcons,
                                            assetPref=assetPreference)

    def updateItems(self):
        super(CgRigSceneModel, self).updateItems()
        # Update the metadata
        for f in self.fileItems:
            f.metadata = cgrigscenefiles.infoDictionary(f.fileNameExt(), f.directory)
            newThumb = cgrigscenefiles.thumbnail(f.fileNameExt(), f.directory)

            if newThumb is None:
                dep = cgrigscenefiles.getDependencyFolder(f.fullPath(), create=True)[0]
                thumbPath = os.path.join(dep, "thumbnail")
                f.thumbnail = self.checkFileImage(thumbPath)

            else:
                f.thumbnail = cgrigscenefiles.thumbnail(f.fileNameExt(), f.directory)

    def checkFileImage(self, filePath):
        """ Checks the jpg or png exists for the filePath.

        :param filePath: File path with the extension excluded.
        :return:
        """
        jpg = filePath + ".jpg"
        png = filePath + ".png"
        if os.path.exists(jpg):
            return jpg
        elif os.path.exists(png):
            return png
        return png
