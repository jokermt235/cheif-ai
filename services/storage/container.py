from injector import Module, provider, singleton
from managers import CustomUserManager

class Container(Module):
    @provider
    def provide_user_service(self) -> CustomUserManager:
        return CustomUserManager()