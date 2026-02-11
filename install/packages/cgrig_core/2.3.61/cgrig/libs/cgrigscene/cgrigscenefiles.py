# -*- coding: utf-8 -*-
import glob
import os
import shutil
from cgrigvendor.six import text_type

from cgrig.libs.utils import path, filesystem, output
from cgrig.core.util import zlogging

from cgrig.libs.cgrigscene import constants
from cgrig.libs.cgrigscene.constants import DEPENDENCY_FOLDER, CGRIG_THUMBNAIL, ASSETTYPES, INFOASSET, INFOCREATORS, \
    INFOWEBSITES, INFOTAGS, INFODESCRIPTION

from cgrig.libs.general.exportglobals import CGRIGSCENESUFFIX, SHADERS, LIGHTS, AREALIGHTS, IBLSKYDOMES, \
    MESHOBJECTS, VERSIONKEY, GENERICVERSIONNO

logger = zlogging.getLogger(__name__)


def thumbnails(directory, fileList):
    """Returns a list of thumbnail image paths from a cgrigScene list without extensions

    :return thumbPathList: List of thumbnail paths one for each cgrigScene file (no extension)
    :rtype thumbFullPathList: list of basestring
    """
    thumbFullPathList = list()
    for i, cgrigSceneFile in enumerate(fileList):
        thumbFullPathList.append(thumbnail(cgrigSceneFile, directory))
    return thumbFullPathList


def thumbnail(cgrigSceneFile, directory):
    """ Get thumbnail from cgrigScene

    :param cgrigSceneFile:
    :param directory:
    :return:
    """
    cgrigSceneFileName = os.path.basename(cgrigSceneFile)
    fileNameNoExt = os.path.splitext(cgrigSceneFileName)[0]
    extension = path.getExtension(cgrigSceneFileName)
    dependFolder = "_".join([fileNameNoExt, extension, DEPENDENCY_FOLDER])
    dependFolderPath = os.path.join(directory, dependFolder)
    if not os.path.isdir(dependFolderPath):
        return None
    imageList = path.getImageNoExtension(dependFolderPath, CGRIG_THUMBNAIL)
    if imageList:  # image list is only thumbnail, take the first image, could be jpg or png
        return os.path.join(dependFolderPath, imageList[0])


def infoDictionaries(cgrigSceneNameList, directory):
    """ Returns a list of info dictionaries for each .cgrigScene file.

    These dictionaries contain information such as author, tag, descriptions etc

    :return infoDictList: A list of info dictionaries for each .cgrigScene file
    :rtype infoDictList: list[dict]
    """
    infoDictList = list()
    if not cgrigSceneNameList:
        return list()
    for cgrigSceneFile in cgrigSceneNameList:
        infoDictList.append(infoDictionary(cgrigSceneFile, directory))
    return infoDictList


def infoDictionary(cgrigSceneFile, directory):
    """ CgRig Info dictionary

    :param cgrigSceneFile:
    :param directory:
    :return:
    """
    fullPath = os.path.join(directory, cgrigSceneFile)
    updateOldFolders(cgrigSceneFile, directory)

    cgrigInfoDict, fileFound = getCgRigInfoFromFile(fullPath, message=False)

    if not fileFound:
        cgrigInfoDict = createEmptyInfoDict()

    cgrigInfoDict['cgrigFilePath'] = fullPath
    cgrigInfoDict['extension'] = path.getExtension(fullPath)
    return cgrigInfoDict


def updateOldFolders(fileName, directoryPath):
    """ Renames dependency folder from old to new "fileName_fileDependency" to "fileName_jpg_fileDependency"

    :param fileName: Path to the file
    :type fileName:
    :return:
    :rtype:
    """

    fileNameNoExt = os.path.splitext(fileName)[0]
    extension = path.getExtension(fileName)
    newDirectory = "_".join([fileNameNoExt, extension, constants.DEPENDENCY_FOLDER])

    # AutoFix old dependency folders
    # Check if one with no extensions exists first and rename that to one with extensions
    newDirectoryNoExt = "_".join([fileNameNoExt, constants.DEPENDENCY_FOLDER])
    dirNoExt = os.path.join(directoryPath, newDirectoryNoExt)
    fullDirPath = os.path.join(directoryPath, newDirectory)

    folderUpdated = False
    if os.path.exists(dirNoExt) and not os.path.exists(fullDirPath):
        os.rename(dirNoExt, fullDirPath)
        folderUpdated = True
    elif os.path.exists(dirNoExt) and os.path.exists(fullDirPath):
        # logger.info("Warning fileDependendies for both source ({}) and destination ({}) exists for \"{}\"".
        #      format(newDirectoryNoExt, newDirectory, cgrigSceneFileName))
        # todo: this needs to handle if both directories already exists (eg move old to new)
        pass

    return folderUpdated


def createEmptyInfoDict():
    """Creates an empty .cgrigInfo dictionary

    :return infoDict: CgRig info dictionary
    :rtype infoDict: dict()
    """
    infoDict = {text_type("assetType"): text_type(""),
                text_type("animation"): text_type(None),
                text_type("description"): text_type(""),
                text_type("version"): text_type("1.0.0"),
                text_type("tags"): text_type(""),
                text_type("creators"): text_type(""),
                text_type("saved"): text_type(list()),
                text_type("websites"): text_type("")
                }
    return infoDict


def renameCgRigSceneOnDisk(newNameNoExtension, filePath, extension=CGRIGSCENESUFFIX):
    """Renames all .cgrigScene re-nameable dependency files on disk, and the .cgrigScene itself
    Also renames the subdir given the newName (no ext)
    will check that the files and directory is writable and error if the files can't be written before renaming

    :param newNameNoExtension: the filename with no extension, will delete all files named this with an extension
    :type newNameNoExtension: str
    :param filePath: the full file path to the cgrig scene including file and extension. Expects cgrigScene, but it doesn't have to be
    :type filePath: str
    :param extension: The file extension
    :type extension: basestring
    :return renamedFullPathFiles: a list of the full paths of the renamed files, can be many dependency files
    :rtype renamedFullPathFiles: list
    """
    notWritableMessage = "This scene cannot be renamed as it's most like in use by Maya or another program"
    if not newNameNoExtension:  # as we don't want to accidentally rename "*" files!
        return
    # get all the files to be renamed and the subDir
    cgrigSceneRelatedFilesFullPath, subDirfullDirPath = getCgRigFiles(filePath)
    # check the new filename does not already exist and get adjust new name with numerical suffix if so
    directoryPath = os.path.dirname(filePath)  # get the dir of the file
    newFullPathFileName = os.path.join(directoryPath, ".".join([newNameNoExtension, extension]))  # new full path
    newFullPathFileName = filesystem.uniqueFileName(newFullPathFileName)  # unique name with numerical suffix
    if not newFullPathFileName:  # very rare
        notWritableMessage = "Cannot be renamed as files already exist and numeric unique name limit hit"
    fileName = os.path.basename(newFullPathFileName)
    newNameNoExtension = os.path.splitext(fileName)[0]
    # If no subdirectory, then rename
    if not subDirfullDirPath:  # then there is no sub dir so just rename the .cgrigscene
        renamedFiles = filesystem.renameMultipleFilesNoExt(newNameNoExtension, [filePath])
        return renamedFiles
    # Check the dir can be renamed, files may not be writable
    if filesystem.checkWritableFile(subDirfullDirPath):  # returns true if not writable
        output.displayWarning(notWritableMessage)
        return
    # Rename the files and subdirectories
    renamedFiles = filesystem.renameMultipleFilesNoExt(newNameNoExtension, cgrigSceneRelatedFilesFullPath)
    if not renamedFiles:
        output.displayWarning(notWritableMessage)
        return
    # rename the folder
    cgrigSceneDir = os.path.dirname(filePath)
    newDirectoryName = "_".join([newNameNoExtension, extension, constants.DEPENDENCY_FOLDER])
    dependencyDir = os.path.join(cgrigSceneDir, newDirectoryName)
    os.rename(subDirfullDirPath, dependencyDir)
    return renamedFiles, dependencyDir


def getDependencyFolder(cgrigSceneFullPath, create=True):
    """creates the dependency directory for .cgrigscene files, these can contain .abc, .info, .obj, .fbx, textures etc

    :param cgrigSceneFullPath: the full path to the .cgrigscene file
    :type cgrigSceneFullPath: str
    :param create: Create if doesn't exist
    :type create: bool
    :return fullDirPath: the full directory path to the new folder
    :rtype fullDirPath: str
    """
    cgrigSceneFileName = os.path.basename(cgrigSceneFullPath)
    directoryPath = os.path.dirname(cgrigSceneFullPath)
    fileNameNoExt = os.path.splitext(cgrigSceneFileName)[0]
    extension = path.getExtension(cgrigSceneFullPath)
    newDirectory = "_".join([fileNameNoExt, extension, constants.DEPENDENCY_FOLDER])
    fullDirPath = os.path.join(directoryPath, newDirectory)

    # Create the dependency folder if it doesnt exist
    if create:  # doesn't already exist
        createDependencies(fullDirPath)
    return fullDirPath, fileNameNoExt


def createDependencies(fullDirPath):
    """ Create dependencies if it doesnt exist

    :param fullDirPath:
    :type fullDirPath:
    :return:
    :rtype:
    """
    if not os.path.exists(fullDirPath):
        os.makedirs(fullDirPath)


def getFileDependenciesList(cgrigScenePath, ignoreThumbnail=False):
    """Retrieve a list of all files in the dependency directory DIRECTORYNAMEDEPENDENCIES
    Files do not have full path so directory path is also returned,
    files are ["fileName.abc", "fileName.cgrigInfo"] etc

    :param cgrigScenePath: the full path to the file usually .cgrigscene but can be any extension
    :type cgrigScenePath: str
    :param ignoreThumbnail: ignores the files called thumbnail.* useful for renaming
    :type ignoreThumbnail: str
    :return fileDependencyList: list of short name files found in the subdirectory DIRECTORYNAMEDEPENDENCIES
    :rtype fileDependencyList: list
    :return fullDirPath: the full path of the sub directory DIRECTORYNAMEDEPENDENCIES
    :rtype fullDirPath: str
    """
    fileDependencyList = list()
    cgrigSceneFileName = os.path.basename(cgrigScenePath)
    directoryPath = os.path.dirname(cgrigScenePath)
    fileNameNoExt = os.path.splitext(cgrigSceneFileName)[0]
    ext = path.getExtension(cgrigScenePath)

    newDirectory = "_".join([fileNameNoExt, ext, constants.DEPENDENCY_FOLDER])
    fullDirPath = os.path.join(directoryPath, newDirectory)
    if not os.path.exists(fullDirPath):  # doesn't already exist
        return fileDependencyList, ""  # return empty as directory doesn't exist
    globPattern = os.path.join(fullDirPath, fileNameNoExt)
    for fileName in glob.glob("{}.*".format(globPattern)):
        fileDependencyList.append(fileName)
    if not ignoreThumbnail:
        for fileName in glob.glob(os.path.join(fullDirPath, "thumbnail.*")):
            fileDependencyList.append(fileName)
    return fileDependencyList, fullDirPath


def getCgRigFiles(filePath, ignoreThumbnail=False):
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
    relatedFiles = [filePath]
    fileDependencyList, subDir = getFileDependenciesList(filePath, ignoreThumbnail=ignoreThumbnail)
    for fileName in fileDependencyList:
        relatedFiles.append(os.path.join(subDir, fileName))
    return relatedFiles, subDir


def getSingleFileFromCgRigScene(cgrigSceneFullPath, fileExtension):
    """ Check if file exists of the extension in cgrigScene dependencies.  Usually looking for a file type.

    Returns the name of the file if it exists given the extension eg .abc from the cgrigSceneFullPath
    Gets all the files in the subdirectory associated with the .cgrigScene file and filters for the file type
    Supports returning of one file, the first it finds so not appropriate for textures

    :param cgrigSceneFullPath:  the full path of the .cgrigScene file to be saved
    :type cgrigSceneFullPath: str
    :param fileExtension:  the file extension to find no ".", so alembic is "abc"
    :type fileExtension: str
    :return extFileName: the filename (no directory) of the extension given > for example "myFileName.abc"
    :rtype extFileName: str
    """
    extFileName = ""
    fileList, directory = getFileDependenciesList(cgrigSceneFullPath)
    if not directory:
        return extFileName
    for fileName in fileList:  # cycle through the files and find if a match with the extension
        if fileName.lower().endswith(fileExtension.lower()):
            return os.path.join(directory, fileName)
    return extFileName


def createTagInfoDict(assetType, creator, website, tags, description, saveInfo, animInfo):
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


def updateCgRigInfo(cgrigSceneFullPath, assetType=ASSETTYPES[0], creator="", website="", tags="", description="",
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
    cgrigInfoDict, fileFound = getCgRigInfoFromFile(cgrigSceneFullPath, message=True)
    # if it does get the current information
    if not fileFound:
        cgrigInfoDict = createTagInfoDict(assetType, creator, website, tags, description, saveInfo, animInfo)
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
    cgrigInfoFullPath = writeCgRigInfo(cgrigSceneFullPath, cgrigInfoDict[constants.INFOASSET],
                                   cgrigInfoDict[constants.INFOCREATORS],
                                   cgrigInfoDict[constants.INFOWEBSITES], cgrigInfoDict[constants.INFOTAGS],
                                   cgrigInfoDict[constants.INFODESCRIPTION],
                                   cgrigInfoDict[constants.INFOSAVE], cgrigInfoDict[constants.INFOANIM],
                                   message=False)
    return cgrigInfoFullPath, cgrigInfoDict


def writeCgRigInfo(cgrigSceneFullPath, assetType, creator, website, tags, description, saveInfo, animInfo, message=True):
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
    cgrigInfoDict = createTagInfoDict(assetType, creator, website, tags, description, saveInfo, animInfo)
    fullDirPath, fileNameNoExt = getDependencyFolder(cgrigSceneFullPath)
    cgrigInfoFileName = ".".join([fileNameNoExt, constants.CGRIG_INFO_EXT])
    cgrigInfoFullPath = os.path.join(fullDirPath, cgrigInfoFileName)
    # Update cgrigInfo file if it already exists, keeps other keys intact ---------------------
    if os.path.exists(cgrigInfoFullPath):
        cgrigInfoDictOld = filesystem.loadJson(cgrigInfoFullPath)
        for key in cgrigInfoDict:
            cgrigInfoDictOld[key] = cgrigInfoDict[key]
        cgrigInfoDict = cgrigInfoDictOld  # Keeps old keys not in the current dict
    # Save -----------------------------
    filesystem.saveJson(cgrigInfoDict, cgrigInfoFullPath, indent=4, separators=(",", ":"), message=False)
    return cgrigInfoFullPath


def getCgRigInfoFromFile(cgrigSceneFullPath, message=True):
    """Gets other files from the .cgrigScene, for example .cgrigInfo from a file on disk

    :param cgrigSceneFullPath: the full path of the cgrigScene file, this will save out as another file cgrigInfo
    :type cgrigSceneFullPath: str
    :return cgrigInfoDict: the dictionary with all info information, if None the file wasn't found
    :rtype cgrigInfoDict: dict
    :return fileFound: was the cgrigInfo file found?
    :rtype fileFound: bool
    """
    cgrigInfoPath = getSingleFileFromCgRigScene(cgrigSceneFullPath, constants.CGRIG_INFO_EXT)
    if not os.path.exists(cgrigInfoPath):  # doesn't exist
        if message:
            output.displayWarning("CgRigInfo File Not Found")
        fileFound = False
        return createTagInfoDict(ASSETTYPES[0], "", "", "", "", "",
                                 ""), fileFound  # return the empty dict as no file found
    fileFound = True
    return filesystem.loadJson(cgrigInfoPath), fileFound  # returns cgrigInfoDict


def deleteCgRigDependencies(filePathCgRigScene, message=True, keepThumbnailOverride=False):
    """Deletes cgrig file dependencies and the .cgrigScene leaving the subDirectory, deletes the actual files on disk.
    Useful for saving over existing files

    :param filePathCgRigScene: The full file path of the .cgrigscene to be deleted, other files are deleted automatically
    :type filePathCgRigScene: str
    :param message: report the message to the user in Maya?
    :type message: bool
    :param keepThumbnailOverride: keeps the existing thumbnail image if over righting, usually for delete when renaming
    :type keepThumbnailOverride: bool
    :return filesFullPathDeleted: The files deleted
    :rtype filesFullPathDeleted: list
    """
    filesFullPathDeleted = list()
    # get all the files to be renamed and the subDir
    cgrigSceneRelatedFilesFullPath, subDirfullDirPath = getCgRigFiles(filePathCgRigScene,
                                                                  ignoreThumbnail=keepThumbnailOverride)
    if filesystem.checkWritableFile(subDirfullDirPath) or filesystem.checkWritableFiles(cgrigSceneRelatedFilesFullPath):
        if message:
            output.displayWarning("This scene cannot be written at this time as it's most like in use by Maya or "
                                  "another program")
        return
    if len(cgrigSceneRelatedFilesFullPath) > 100:
        output.displayWarning("This function is deleting more than 100 files!! "
                              "something is wrong, check the files in dir `{}`".format(subDirfullDirPath))
        return
    for fileFullPath in cgrigSceneRelatedFilesFullPath:
        os.remove(fileFullPath)
        filesFullPathDeleted.append(fileFullPath)
    return filesFullPathDeleted


def deleteCgRigSceneFiles(fileFullPath, message=True, keepThumbnailOverride=False):
    """Deletes a file and it's related dependencies on disk, usually a .cgrigScene but can have any extension

    :param fileFullPath: The full file path of the file to be deleted, dependency files are deleted automatically
    :type fileFullPath: str
    :param message: report the message to the user in Maya?
    :type message: bool
    :param keepThumbnailOverride: If True will skip the thumbnail image deletion. Used while renaming.
    :type keepThumbnailOverride: bool
    :return filesFullPathDeleted: The files deleted
    :rtype filesFullPathDeleted: list
    """
    filesFullPathDeleted = list()
    # get all the files to be renamed and the subDir
    cgrigSceneRelatedFilesFullPath, subDirfullDirPath = getCgRigFiles(fileFullPath)
    if keepThumbnailOverride:
        if "thumbnail.jpg" in cgrigSceneRelatedFilesFullPath:
            cgrigSceneRelatedFilesFullPath.remove("thumbnail.jpg")
        if "thumbnail.png" in cgrigSceneRelatedFilesFullPath:
            cgrigSceneRelatedFilesFullPath.remove("thumbnail.png")
    if not subDirfullDirPath:  # there's no subdirectory so just delete the file and return it
        # doesn't need a check as it should be deletable
        os.remove(fileFullPath)
        filesFullPathDeleted.append(fileFullPath)
        return filesFullPathDeleted
    # check the files and dir file-permissions, rename of itself to the same name, returns true if not writable
    if filesystem.checkWritableFile(subDirfullDirPath) or filesystem.checkWritableFiles(cgrigSceneRelatedFilesFullPath):
        if message:
            output.displayWarning("This scene cannot be deleted/renamed as it's most like in use by Maya or "
                                  "another program")
        return
    if len(cgrigSceneRelatedFilesFullPath) > 20:
        output.displayWarning("This function is deleting more than 20 files!! "
                              "something is wrong, check the files in dir `{}`".format(subDirfullDirPath))
        return
    for fileFullPath in cgrigSceneRelatedFilesFullPath:
        os.remove(fileFullPath)
        filesFullPathDeleted.append(fileFullPath)
    # delete subdir
    if not keepThumbnailOverride:
        shutil.rmtree(subDirfullDirPath)
    filesFullPathDeleted.append(subDirfullDirPath)
    return filesFullPathDeleted


def updateCgRigSceneDir(directory):
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


def writeCgRigGShaders(cgrigShaderDict, cgrigSceneFullPath):
    """Writes a shader dict to disk in the cgrig dependency sub folder

    :param cgrigShaderDict: the generic shader dictionary
    :type cgrigShaderDict: dict
    :param cgrigSceneFullPath: the full path to the cgrigScene file
    :type cgrigSceneFullPath: str
    :return cgrigShadFullPath: the full path to the shader file that has been saved
    :rtype cgrigShadFullPath: str
    """
    fullDirPath, fileNameNoExt = getDependencyFolder(cgrigSceneFullPath)
    cgrigShadFileName = ".".join([fileNameNoExt, constants.CGRIG_SHADER_EXT])
    cgrigShadFullPath = os.path.join(fullDirPath, cgrigShadFileName)
    filesystem.saveJson(cgrigShaderDict, cgrigShadFullPath, indent=4, separators=(",", ":"))
    return cgrigShadFullPath


def writeCgRigGLights(cgrigLightsDict, cgrigSceneFullPath):
    """Writes a light dict to disk inside the cgrig dependency sub folder of the given .cgrigScene file

    :param cgrigLightsDict: the generic lights dictionary
    :type cgrigLightsDict: dict
    :param cgrigSceneFullPath: the full path to the cgrigScene file
    :type cgrigSceneFullPath: str
    :return cgrigShadFullPath: the full path to the shader file that has been saved
    :rtype cgrigShadFullPath: str
    """
    fullDirPath, fileNameNoExt = getDependencyFolder(cgrigSceneFullPath)
    cgrigLightsFileName = ".".join([fileNameNoExt, constants.CGRIG_LIGHT_EXT])
    cgrigLightsFullPath = os.path.join(fullDirPath, cgrigLightsFileName)
    filesystem.saveJson(cgrigLightsDict, cgrigLightsFullPath, indent=4, separators=(",", ":"))
    return cgrigLightsFullPath


def writeExportCgRigInfo(cgrigSceneFullPath, cgrigSceneDict, gShaderDict, gLightDict, objectRootList, tagInfoDict,
                       animationInfo):
    """While exporting writes the .cgrigInfo file
    Should add cameras

    :param cgrigSceneFullPath: full path the the .cgrigScene
    :type cgrigSceneFullPath: str
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
        tagInfoDict = createTagInfoDict(ASSETTYPES[0], "", "", "", "", "", "")
    cgrigInfoFullPath = writeCgRigInfo(cgrigSceneFullPath, tagInfoDict[INFOASSET], tagInfoDict[INFOCREATORS],
                                   tagInfoDict[INFOWEBSITES], tagInfoDict[INFOTAGS], tagInfoDict[INFODESCRIPTION],
                                   fileInfoSaved, animationInfo)
    return cgrigInfoFullPath, fileInfoSaved


def loadGenericShaderLightFiles(cgrigSceneFullPath):
    """loads a .cgrigGShad and .cgrigGLight information from a cgrigSceneFullPath

    :param cgrigSceneFullPath: the full path to the .cgrigScene file
    :type cgrigSceneFullPath: str
    :return shadMultDict: the generic shader dictionary
    :rtype shadMultDict: dict
    :return lightMultDict: the generic light dictionary
    :rtype lightMultDict: dict
    """
    shadMultDict = dict()
    lightMultDict = dict()
    directoryPath = getDependencyFolder(cgrigSceneFullPath)[0]  # just pull the path and not the filename
    if not directoryPath:  # could not find folder so dicts are empty
        return shadMultDict, lightMultDict
    lightFile = getSingleFileFromCgRigScene(cgrigSceneFullPath,
                                          constants.CGRIG_LIGHT_EXT)  # the filename only no path
    shaderFile = getSingleFileFromCgRigScene(cgrigSceneFullPath, constants.CGRIG_SHADER_EXT)
    if shaderFile:
        shaderFullPath = os.path.join(directoryPath, shaderFile)
        if os.path.isfile(shaderFullPath):
            shadMultDict = filesystem.loadJson(shaderFullPath)
    if lightFile:
        lightFullPath = os.path.join(directoryPath, lightFile)
        if os.path.isfile(lightFullPath):
            lightMultDict = filesystem.loadJson(lightFullPath)
    return shadMultDict, lightMultDict
