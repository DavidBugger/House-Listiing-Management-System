
def user_property_directory_path(instance, filename):
    return 'user_{0}/property/{1}'.format(instance.seller.users.id, filename)