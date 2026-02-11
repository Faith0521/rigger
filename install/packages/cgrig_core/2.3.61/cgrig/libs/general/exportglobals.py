# -*- coding: utf-8 -*-

GENERICVERSIONNO = "1.1.0"  # the version number of the generic file format

CGRIGSCENESUFFIX = "cgrigScene"

VERSIONKEY = "version"  # the key (name) of the version component of a generic dict
LIGHTS = "lightDict"  # the key (name) of the light component of a generic dict
SHADERS = "shaderDict"  # the key (name) of the shader component of a generic dict
MESHOBJECTS = "meshObjects"  # the key (name) of the mesh object dict

AREALIGHTS = "areaLights"
IBLSKYDOMES = "iblSkydomes"
DIRECTIONALS = "directionalLights"

NAMESPACELIST = "namespaces"  # the key for recording all namespaces in the scene

SMOOTHLEVEL = "smoothLevel"  # SubD attribute and dict key
DISPLAYSMOOTHMESH = "displaySmoothMesh"  # SubD attribute and dict key
USESMOOTHPREVIEWFORRENDERER = "useSmoothPreviewForRender"  # SubD attribute and dict key
RENDERSMOOTHLEVEL = "renderSmoothLevel"  # SubD attribute and dict key

ARNOLD = "Arnold"
REDSHIFT = "Redshift"
RENDERMAN = "Renderman"
VIEWPORT2 = "Viewport"  # todo "Viewport" should become "Maya" and be phased out
VRAY = "VRay"
MAYA = "Maya"
UNKNOWN = ""
ALL = "All"
GENERIC = "Generic"

SUPPORTEDRENDERERLIST = [REDSHIFT, RENDERMAN, ARNOLD]

LOCGRPNAME = "lightMatchLocs_grp"
LIGHTGRPNAME = "Lights_grp"

# CGRIG ABC ATTRIBUTES for alembic
CGRIGABC_MESH = "cgrigABC_mesh"
CGRIGABC_LIGHT = "cgrigABC_light"
CGRIGABC_CAM = "cgrigABC_camera"
CGRIGABC_LOC = "cgrigABC_locator"
CGRIGABC_CURVE = "cgrigABC_curve"
CGRIGABC_PREFIX = "cgrigABC"

RENDERMANAREALIGHTTYPES = ("PxrRectLight", "PxrSphereLight", "PxrDiskLight")

RENDERERAREALIGHTS = {REDSHIFT: "RedshiftPhysicalLight",
                      RENDERMAN: RENDERMANAREALIGHTTYPES,
                      ARNOLD: "aiAreaLight"}

RENDERERDIRECTIONALLIGHTS = {REDSHIFT: "directionalLight",
                             RENDERMAN: "PxrDistantLight",
                             ARNOLD: "directionalLight"}

RENDERERSKYDOMELIGHTS = {REDSHIFT: "RedshiftDomeLight",
                         RENDERMAN: "PxrDomeLight",
                         ARNOLD: "aiSkyDomeLight"}

THUMBNAIL = "thumbnail"