from _commons.api.exceptions import PermissionCodeError, BusinessLogicError


class InternalInfoMixin(object):
    internal = "This means..."
    more_info = "https://drive.google.com/drive/u/0/folders/0B8WnfaHtXP4QfkgxZ1hEcUJTN0VsbHgweXNuMG1jZlpIbHJRUlIxZXhOb0JTdmNpbWg4OGM"


class UTP0001_INVALID_LOGIN(InternalInfoMixin, PermissionCodeError):
    message = "The email and password you entered don't match."


class UTP0002_SUSPENDED_ACCOUNT(InternalInfoMixin, PermissionCodeError):
    message = "Your account has been suspended. If you have any question, please contact us on Hillotask.com/support"

class UTP0002_UNVARIFY_ACCOUNT(InternalInfoMixin,PermissionCodeError):
	message = "You account has not been activated yet, please verify your email first. "

class UTB0001_INVALID_EMAIL(InternalInfoMixin, BusinessLogicError):
    message = "It seems that we have not reached your university yet. Please contact us on Hillotask.com/support to sign up your university!"

class UTP0003_INVALID_AUTH_TOKEN(InternalInfoMixin, PermissionCodeError):
	message = "You Must be Logged-in to See this."

class UTP0004_INVALID_CODE(InternalInfoMixin, BusinessLogicError):
	message = "Your input Invitation Code is Invalid."