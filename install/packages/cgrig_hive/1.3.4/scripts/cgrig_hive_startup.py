
def startup(package):
    """ Set up environmental variables depending on DCC
    """
    from cgrig.preferences.interfaces import hiveinterfaces
    hiveInterface = hiveinterfaces.hiveInterface()
    hiveInterface.upgradePreferences()
    hiveInterface.upgradeAssets()
    try:
        from cgrig.libs.hive.base import configuration
        configuration.Configuration()
    except ImportError:
        print("Hive has not loaded as part of this maya session, ignoring preloading")
