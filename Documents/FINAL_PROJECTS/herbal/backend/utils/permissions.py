def has_role(user, role):
    return user.groups.filter(name=role).exists()


def is_admin(user):
    return has_role(user, "Admin")


def is_data_manager(user):
    return has_role(user, "Data Manager")


def is_data_clerk(user):
    return has_role(user, "Data Clerk")


def is_reviewer(user):
    return has_role(user, "Reviewer")


def is_monitor(user):
    return has_role(user, "Monitor")


def is_pi(user):
    return has_role(user, "PI")
