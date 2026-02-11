# -*- coding: utf-8 -*-
import glob
import os
from os import path

from cgrig.libs.general.exportglobals import CGRIGSCENESUFFIX, VERSIONKEY, GENERICVERSIONNO, SHADERS, LIGHTS, AREALIGHTS, \
    IBLSKYDOMES, MESHOBJECTS
from cgrig.libs.utils import path, filesystem, output
from cgrig.libs.cgrigscene import constants
from cgrig.libs.cgrigscene.constants import DEPENDENCY_FOLDER, CGRIG_THUMBNAIL, ASSETTYPES, INFOASSET, INFOCREATORS, \
    INFOWEBSITES, INFOTAGS, INFODESCRIPTION


class CgRigScene(object):
    def __init__(self, path=None, extension=CGRIGSCENESUFFIX):
        """

        :param path:
        """
        self.path = path
        self.extension = extension

        # Info
        self.assetType = ""
        self.animation = None
        self.description = ""
        self.version = "1.0.0"
        self.tags = ""
        self.creators = ""
        self.saved = []
        self.websites = ""

    def dependencyFolder(self, create=True):
        """ Get the dependency folder the .cgrigscene files

        - These can contain .abc, .info, .obj, .fbx, textures etc

        :param create: Create if doesn't exist
        :type create: bool
        :return fullDirPath: the full directory path to the new folder
        :rtype fullDirPath: str
        """
        cgrigSceneFileName = os.path.basename(self.path)
        directoryPath = os.path.dirname(self.path)
        fileNameNoExt = os.path.splitext(cgrigSceneFileName)[0]
        extension = path.getExtension(self.path)
        newDirectory = "_".join([fileNameNoExt, extension, constants.DEPENDENCY_FOLDER])
        fullDirPath = os.path.join(directoryPath, newDirectory)

        # Create the dependency folder if it doesnt exist
        if create and not os.path.exists(fullDirPath):  # doesn't already exist
            os.makedirs(fullDirPath)
        return fullDirPath, fileNameNoExt

    def directory(self):
        return os.path.dirname(self.path)

    def fileName(self):
        return os.path.basename(self.path)

    def fileNameNoExt(self):
        return os.path.splitext(self.fileName())[0]

    def dependencyFiles(self, ignoreThumbnail=False):
        """ Retrieve a list of all files in the dependency directory DIRECTORYNAMEDEPENDENCIES
        Files do not have full path so directory path is also returned,
        files are ["fileName.abc", "fileName.cgrigInfo"] etc

        :param ignoreThumbnail: ignores the files called thumbnail.* useful for renaming
        :type ignoreThumbnail: str
        :return fileDependencyList: list of short name files found in the subdirectory DIRECTORYNAMEDEPENDENCIES
        :rtype fileDependencyList: list
        :return fullDirPath: the full path of the sub directory DIRECTORYNAMEDEPENDENCIES
        :rtype fullDirPath: str
        """
        fileDependencyList = list()
        fileNameNoExt = os.path.splitext(self.fileName())[0]
        ext = path.getExtension(self.path)

        newDirectory = "_".join([fileNameNoExt, ext, constants.DEPENDENCY_FOLDER])
        fullDirPath = os.path.join(self.directory(), newDirectory)
        if not os.path.exists(fullDirPath):  # doesn't already exist
            return fileDependencyList, ""  # return empty as directory doesn't exist
        globPattern = os.path.join(fullDirPath, fileNameNoExt)
        for fileName in glob.glob("{}.*".format(globPattern)):
            fileDependencyList.append(fileName)
        if not ignoreThumbnail:
            for fileName in glob.glob(os.path.join(fullDirPath, "thumbnail.*")):
                fileDependencyList.append(fileName)

        return fileDependencyList, fullDirPath

    def thumbnailPath(self):
        """ Gets the thumbnail path, usually in the dependency folder

        :return:
        """
        fileNameNoExt = self.fileNameNoExt()
        dependFolder = "_".join([fileNameNoExt, self.extension, DEPENDENCY_FOLDER])
        dependFolderPath = os.path.join(self.directory(), dependFolder)
        if not os.path.isdir(dependFolderPath):
            return None

        files, dirPath = self.dependencyFiles()
        length = len(CGRIG_THUMBNAIL)
        for f in files:
            if CGRIG_THUMBNAIL in f and f[:length] == CGRIG_THUMBNAIL and path.imageSupportByQt(os.path.join(dirPath, f)):
                return f

    def getCgRigFiles(self, ignoreThumbnail=False):
        """ Retrieves all cgrig files related to the given file (usually .cgrigscene).

        Expects .cgrigscene file but can be any file under the main folder that has file dependencies

        returns only filenames not the directory path

        :param filePath: full path of a .cgrigscene file or a file in the main folder
        :type filePath: basestring
        :param ignoreThumbnail: ignores the files called thumbnail.* useful for renaming
        :type ignoreThumbnail: str
        :return relatedFiles, subDir: all files related to the .cgrigscene in the current directory as string paths, and the dependency subdirectory
        :rtype relatedFiles: tuple(list[basestring], basestring)
        """
        relatedFiles = [self.path]
        fileDependencyList, subDir = self.dependencyFiles(ignoreThumbnail=ignoreThumbnail)
        # todo get files based on extension
        for fileName in fileDependencyList:
            relatedFiles.append(os.path.join(subDir, fileName))
        return relatedFiles, subDir  # todo create CgRigScene object for each one

    def getSingleFileFromCgRigScene(self, fileExtension):
        """ Check if file exists in cgrigScene dependencies

        Returns the name of the file if it exists given the extension eg .abc from the cgrigSceneFullPath
        Gets all the files in the subdirectory associated with the .cgrigScene file and filters for the file type
        Supports returning of one file, the first it finds so not appropriate for textures


        :param fileExtension:  the file extension to find no ".", so alembic is "abc"
        :type fileExtension: str
        :return extFileName: the filename (no directory) of the extension given > for example "myFileName.abc"
        :rtype extFileName: str
        """

        extFileName = ""
        fileList, directory = self.dependencyFiles()
        if not directory:
            return extFileName
        for fileName in fileList:  # cycle through the files and find if a match with the extension
            if fileName.lower().endswith(fileExtension.lower()):
                return os.path.join(directory, fileName)
        return extFileName

    def createTagInfoDict(self, assetType, creator, website, tags, description, saveInfo, animInfo):
        """ Creates a dict ready for the cgrigInfo file

        :param assetType: the information about asset type, model, scene, lights, shaders, etc
        :type assetType: str
        :param creator: the information about creator/s
        :type creator: str
        :param website: the information about the creators website links
        :type website: str
        :param tags: the tag information
        :type tags: str
        :param description: the full description
        :type description: str
        :param saveInfo: the file information saved as a list ["alembic", "generic lights"] etc
        :type saveInfo: list
        :param animInfo: the animation information of the file "0 100" or "" or None if none
        :type animInfo: str
        :return cgrigInfoDict: the dict containing all information including the file version number
        :rtype cgrigInfoDict: str
        """
        cgrigInfoDict = {constants.INFOASSET: assetType,
                       constants.INFOCREATORS: creator,
                       constants.INFOWEBSITES: website,
                       constants.INFOTAGS: tags,
                       constants.INFODESCRIPTION: description,
                       constants.INFOSAVE: saveInfo,
                       constants.INFOANIM: animInfo,
                       VERSIONKEY: GENERICVERSIONNO}
        return cgrigInfoDict

    def updateCgRigInfo(self, assetType=ASSETTYPES[0], creator="", website="", tags="", description="",
                      saveInfo="", animInfo=""):
        """Updates the .cgrigInfo file depending on the incoming values, if not variable then leave the values as are.

        :param cgrigSceneFullPath: the full path of the cgrigScene file, this will save out as another file cgrigInfo
        :type cgrigSceneFullPath: str
        :param assetType: the information about asset type, model, scene, lights, shaders, etc
        :type assetType: str
        :param creator: the information about creator/s
        :type creator: str
        :param website: the information about the creators website links
        :type website: str
        :param tags: the tag information
        :type tags: str
        :param description: the full description
        :type description: str
        :param saveInfo: the file information saved as a list ["alembic", "generic lights"] etc
        :type saveInfo: list
        :param animInfo: the animation information of the file "0 100" or "" or None if none
        :type animInfo: str
        :return cgrigInfoFullPath: the full path of the .cgrigInfo file
        :rtype cgrigInfoFullPath: str
        :return cgrigInfoDict: the dict containing all information including the file version number
        :rtype cgrigInfoDict: str
        """
        # find if the .cgrigInfo file exists
        cgrigInfoDict, fileFound = self.getCgRigInfoFromFile(message=True)
        # if it does get the current information
        if not fileFound:
            cgrigInfoDict = self.createTagInfoDict(assetType, creator, website, tags, description, saveInfo, animInfo)
        else:
            if assetType != ASSETTYPES[0]:  # if not default "Not Specified"
                cgrigInfoDict[constants.INFOASSET] = assetType
            if creator:
                cgrigInfoDict[constants.INFOCREATORS] = creator
            if website:
                cgrigInfoDict[constants.INFOWEBSITES] = website
            if tags:
                cgrigInfoDict[constants.INFOTAGS] = tags
            if description:
                cgrigInfoDict[constants.INFODESCRIPTION] = description
            if saveInfo:
                cgrigInfoDict[constants.INFODESCRIPTION] = saveInfo
            if animInfo:
                cgrigInfoDict[constants.INFODESCRIPTION] = animInfo
        # save the updated dict
        cgrigInfoFullPath = self.writeCgRigInfo(cgrigInfoDict[constants.INFOASSET],
                                            cgrigInfoDict[constants.INFOCREATORS],
                                            cgrigInfoDict[constants.INFOWEBSITES], cgrigInfoDict[constants.INFOTAGS],
                                            cgrigInfoDict[constants.INFODESCRIPTION],
                                            cgrigInfoDict[constants.INFOSAVE], cgrigInfoDict[constants.INFOANIM],
                                            message=False)
        return cgrigInfoFullPath, cgrigInfoDict

    def writeCgRigInfo(self, assetType, creator, website, tags, description, saveInfo, animInfo,
                     message=True):
        """Saves a cgrigInfo file in the subdirectory from the cgrigScene file

        :param cgrigSceneFullPath: the full path of the cgrigScene file, this will save out as another file cgrigInfo
        :type cgrigSceneFullPath: str
        :param assetType: the information about asset type, model, scene, lights, shaders, etc
        :type assetType: str
        :param creator: the information about creator/s
        :type creator: str
        :param website: the information about the creators website links
        :type website: str
        :param tags: the tag information
        :type tags: str
        :param description: the full description
        :type description: str
        :param saveInfo: the save info list, what did the file save?
        :type saveInfo: list
        :param animInfo:
        :type animInfo:
        :param message: report the save success message to the user?
        :type message: bool

        :return cgrigInfoFullPath: the full path of the file saved (cgrigInfo)
        :rtype cgrigInfoFullPath:
        """
        cgrigInfoDict = self.createTagInfoDict(assetType, creator, website, tags, description, saveInfo, animInfo)
        fullDirPath, fileNameNoExt = self.dependencyFolder()
        cgrigInfoFileName = ".".join([fileNameNoExt, constants.CGRIG_INFO_EXT])
        cgrigInfoFullPath = os.path.join(fullDirPath, cgrigInfoFileName)
        filesystem.saveJson(cgrigInfoDict, cgrigInfoFullPath, indent=4, separators=(",", ":"), message=False)
        return cgrigInfoFullPath

    def getCgRigInfoFromFile(self, message=True):
        """Gets other files from the .cgrigScene, for example .cgrigInfo from a file on disk

        :param cgrigSceneFullPath: the full path of the cgrigScene file, this will save out as another file cgrigInfo
        :type cgrigSceneFullPath: str
        :return cgrigInfoDict: the dictionary with all info information, if None the file wasn't found
        :rtype cgrigInfoDict: dict
        :return fileFound: was the cgrigInfo file found?
        :rtype fileFound: bool
        """
        cgrigInfoPath = self.getSingleFileFromCgRigScene(constants.CGRIG_INFO_EXT)
        if not os.path.exists(cgrigInfoPath):  # doesn't exist
            if message:
                output.displayWarning("CgRigInfo File Not Found")
            fileFound = False
            return self.createTagInfoDict(ASSETTYPES[0], "", "", "", "", "",
                                     ""), fileFound  # return the empty dict as no file found
        fileFound = True
        return filesystem.loadJson(cgrigInfoPath), fileFound  # returns cgrigInfoDict

    def deleteDependencies(self, keepThumbnailOverride=False, message=True):
        """Deletes cgrig file dependencies and the .cgrigScene leaving the subDirectory, deletes the actual files on disk.
        Useful for saving over existing files

        :param message: report the message to the user in Maya?
        :type message: bool
        :param keepThumbnailOverride: keeps the existing thumbnail image if over righting, usually for delete when renaming
        :type keepThumbnailOverride: bool
        :return filesFullPathDeleted: The files deleted
        :rtype filesFullPathDeleted: list
        """
        deletedPaths = list()  # List of file paths that were deleted
        # get all the files to be renamed and the subDir
        paths, directory = self.getCgRigFiles(ignoreThumbnail=keepThumbnailOverride)
        if filesystem.checkWritableFile(directory) or filesystem.checkWritableFiles(paths):
            if message:
                output.displayWarning("This scene cannot be written at this time as it's most like in use by Maya or "
                                      "another program")
            return
        if len(paths) > 100:
            output.displayWarning("This function is deleting more than 100 files!! "
                                  "something is wrong, check the files in dir `{}`".format(directory))
            return
        for fileFullPath in paths:
            os.remove(fileFullPath)
            deletedPaths.append(fileFullPath)
        return deletedPaths

    def delete(self, message=True, keepThumbnailOverride=False):
        """Deletes a file and it's related dependencies on disk, usually a .cgrigScene but can have any extension

        The full file path of the file to be deleted, dependency files are deleted automatically

        :param message: report the message to the user in Maya?
        :type message: bool
        :param keepThumbnailOverride: If True will skip the thumbnail image deletion. Used while renaming.
        :type keepThumbnailOverride: bool
        :return filesFullPathDeleted: The files deleted in the format of absolute paths
        :rtype filesFullPathDeleted: list
        """
        deletedFiles = list()
        # get all the files to be renamed and the subDir
        cgrigPaths, dependencyDir = self.getCgRigFiles()
        if keepThumbnailOverride:
            if "thumbnail.jpg" in cgrigPaths:
                cgrigPaths.remove("thumbnail.jpg")
            if "thumbnail.png" in cgrigPaths:
                cgrigPaths.remove("thumbnail.png")
        if not dependencyDir:  # there's no subdirectory so just delete the file and return it
            # doesn't need a check as it should be deletable
            os.remove(self.path)
            deletedFiles.append(self.path)
            return deletedFiles
        # check the files and dir file-permissions, rename of itself to the same name, returns true if not writable
        if filesystem.checkWritableFile(dependencyDir) or filesystem.checkWritableFiles(cgrigPaths):
            if message:
                output.displayWarning("This scene cannot be deleted/renamed as it's most like in use by Maya or "
                                      "another program")
            return
        if len(cgrigPaths) > 20:
            output.displayWarning("This function is deleting more than 20 files!! "
                                  "something is wrong, check the files in dir `{}`".format(dependencyDir))
            return
        for fileFullPath in cgrigPaths:
            os.remove(fileFullPath)
            deletedFiles.append(fileFullPath)
        # delete subdir
        if not keepThumbnailOverride:
            os.rmdir(dependencyDir)
        deletedFiles.append(dependencyDir)
        return deletedFiles

    def updateCgRigSceneDir(self, directory):
        """Updates .cgrig Scenes from pre v1 format where generic light and shader data was saved inside the .cgrigScene
        Will batch all .cgrigScene files in the given directory and fix them from the old format

        :param directory:
        :type directory:
        """
        # get a list of the .cgrigScenes
        cgrigSceneList = list()
        for fileName in glob.glob("{}/*.{}".format(directory, CGRIGSCENESUFFIX)):
            cgrigSceneList.append(fileName)
        # start loop
        for cgrigScene in cgrigSceneList:
            cgrigSceneFullPath = os.path.join(directory, cgrigScene)
            cgrigSceneDict = filesystem.loadJson(cgrigSceneFullPath)
            if SHADERS in cgrigSceneDict:
                shaderDict = cgrigSceneDict[SHADERS]
            else:
                shaderDict = dict()
            lightDict = cgrigSceneDict[LIGHTS]
            # see if the directory dependancies exists if not create it
            getDependencyFolder(cgrigSceneFullPath)
            # create the shader dict and the light dict files if they exists
            if lightDict[AREALIGHTS] or lightDict[IBLSKYDOMES]:
                # create the light dict
                writeCgRigGLights(lightDict, cgrigSceneFullPath)
            if shaderDict:
                # create the shader dict
                writeCgRigGShaders(shaderDict, cgrigSceneFullPath)
            # remove the shader and light dicts
            cgrigSceneDict.pop(SHADERS, None)
            cgrigSceneDict.pop(LIGHTS, None)
            filesystem.saveJson(cgrigSceneDict, cgrigSceneFullPath, indent=4, separators=(",", ":"))

    def writeExportCgRigInfo(self, cgrigSceneDict, gShaderDict, gLightDict, objectRootList, tagInfoDict,
                           animationInfo):
        """While exporting writes the .cgrigInfo file
        Should add cameras

        :param cgrigSceneDict: the dictionary that will be written to the .cgrigScene
        :type cgrigSceneDict: dict
        :param objectRootList: the scene roots from alemebic
        :type objectRootList: list
        :param tagInfoDict: the tag info if provided ok if it's empty, this will be written
        :type tagInfoDict: dict
        :return cgrigInfoFullPath: the full path to the cgrigInfo file
        :rtype cgrigInfoFullPath: str
        :return fileInfoSaved: the info list with what was saved
        :rtype fileInfoSaved: list
        """
        fileInfoSaved = list()
        if objectRootList:
            fileInfoSaved.append(constants.SAVE_ALEMBIC)
        if gShaderDict:
            fileInfoSaved.append(constants.SAVE_G_SHADERS)
        if gLightDict:
            fileInfoSaved.append(constants.SAVE_LIGHTS)
        if MESHOBJECTS in cgrigSceneDict:
            if cgrigSceneDict[MESHOBJECTS]:
                fileInfoSaved.append(constants.SAVE_MESH)
        if not tagInfoDict:  # create an empty dict to pass in
            # ASSETTYPES[0] is "Not Specified"
            tagInfoDict = self.createTagInfoDict(ASSETTYPES[0], "", "", "", "", "", "")
        cgrigInfoFullPath = self.writeCgRigInfo(tagInfoDict[INFOASSET], tagInfoDict[INFOCREATORS],
                                            tagInfoDict[INFOWEBSITES], tagInfoDict[INFOTAGS],
                                            tagInfoDict[INFODESCRIPTION],
                                            fileInfoSaved, animationInfo)
        return cgrigInfoFullPath, fileInfoSaved


class CgRigSceneLights(CgRigScene):

    def writeCgRigGLights(self, cgrigLightsDict):
        """Writes a light dict to disk inside the cgrig dependency sub folder of the given .cgrigScene file
        todo subclass

        :param cgrigLightsDict: the generic lights dictionary
        :type cgrigLightsDict: dict
        :param cgrigSceneFullPath: the full path to the cgrigScene file
        :type cgrigSceneFullPath: str
        :return cgrigShadFullPath: the full path to the shader file that has been saved
        :rtype cgrigShadFullPath: str
        """
        fullDirPath, fileNameNoExt = self.dependencyFolder()
        cgrigLightsFileName = ".".join([fileNameNoExt, constants.CGRIG_LIGHT_EXT])
        cgrigLightsFullPath = os.path.join(fullDirPath, cgrigLightsFileName)
        filesystem.saveJson(cgrigLightsDict, cgrigLightsFullPath, indent=4, separators=(",", ":"))
        return cgrigLightsFullPath


class CgRigSceneShader(CgRigScene):
    def loadGenericShaderLightFiles(self):
        """loads a .cgrigGShad and .cgrigGLight information from a cgrigSceneFullPath
        todo subclass

        :param cgrigSceneFullPath: the full path to the .cgrigScene file
        :type cgrigSceneFullPath: str
        :return shadMultDict: the generic shader dictionary
        :rtype shadMultDict: dict
        :return lightMultDict: the generic light dictionary
        :rtype lightMultDict: dict
        """
        shadMultDict = dict()
        lightMultDict = dict()
        directoryPath = self.dependencyFolder()[0]  # just pull the path and not the filename
        if not directoryPath:  # could not find folder so dicts are empty
            return shadMultDict, lightMultDict
        lightFile = self.getSingleFileFromCgRigScene(constants.CGRIG_LIGHT_EXT)  # the filename only no path
        shaderFile = self.getSingleFileFromCgRigScene(constants.CGRIG_SHADER_EXT)
        if shaderFile:
            shaderFullPath = os.path.join(directoryPath, shaderFile)
            if os.path.isfile(shaderFullPath):
                shadMultDict = filesystem.loadJson(shaderFullPath)
        if lightFile:
            lightFullPath = os.path.join(directoryPath, lightFile)
            if os.path.isfile(lightFullPath):
                lightMultDict = filesystem.loadJson(lightFullPath)
        return shadMultDict, lightMultDict

    def writeCgRigGShaders(self, cgrigShaderDict):
        """Writes a shader dict to disk in the cgrig dependency sub folder

        :param cgrigShaderDict: the generic shader dictionary
        :type cgrigShaderDict: dict
        :param cgrigSceneFullPath: the full path to the cgrigScene file
        :type cgrigSceneFullPath: str
        :return cgrigShadFullPath: the full path to the shader file that has been saved
        :rtype cgrigShadFullPath: str
        """
        fullDirPath, fileNameNoExt = self.dependencyFolder()
        cgrigShadFileName = ".".join([fileNameNoExt, constants.CGRIG_SHADER_EXT])
        cgrigShadFullPath = os.path.join(fullDirPath, cgrigShadFileName)
        filesystem.saveJson(cgrigShaderDict, cgrigShadFullPath, indent=4, separators=(",", ":"))
        return cgrigShadFullPath
