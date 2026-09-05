from enum import Enum, IntEnum, IntFlag, StrEnum, auto, unique

__all__ = ["HttpCode", "Permission", "Role", "Status"]


# enforce unique values across all members
@unique
class Status(Enum):
    PENDING = 1
    IN_PROGRESS = 2
    COMPLETED = 3
    FAILED = 4


@unique
class HttpCode(IntEnum):
    OK = 200
    NOT_FOUND = 404


@unique
class Role(StrEnum):
    ADMIN = "admin"
    USER = "user"

    def prefix_upper(self) -> str:
        return self.value[0].upper() + self.value[1:]


@unique
class Permission(IntFlag):
    # auto value assignment
    READ = auto()
    WRITE = auto()
    EXEC = auto()


def main() -> None:
    current_status = Status.COMPLETED
    print(current_status.name)
    print(current_status.value)
    print(current_status is Status.FAILED)
    print(current_status == Status.FAILED)
    print(current_status is Status.COMPLETED)
    print(current_status == Status.COMPLETED)
    print()
    print(f"{Status.PENDING == 1}; {HttpCode.OK == 200}; {Role.ADMIN == 'admin'}")
    print(Role.ADMIN.prefix_upper())
    print()
    user_permissions = Permission.READ | Permission.WRITE
    print(f"{Permission.READ.value}, {Permission.WRITE.value}, {Permission.EXEC.value}")
    print(f"{user_permissions.name}, {user_permissions.value}")
    print(Permission.EXEC in user_permissions)


if __name__ == "__main__":
    main()
