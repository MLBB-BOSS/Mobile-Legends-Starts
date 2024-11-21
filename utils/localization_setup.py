from .localization import LocalizationManager

def get_localization_instance(locale: str = "uk") -> LocalizationManager:
    return LocalizationManager(locale)
