
def get_project_settings() -> str:
    project_settings = None
    try:    
        from local import project_settings as project_settings
    except ModuleNotFoundError:
        project_settings = 'repositext.settings'
    return project_settings
