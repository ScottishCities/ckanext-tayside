from ckan.plugins import toolkit


def user_names_exists(user_names, context):
    model = context['model']
    session = context['session']
    user_names = user_names.split(',')

    for user_name in user_names:
        result = session.query(model.User).filter_by(name=user_name).first()
        if not result:
            raise toolkit.Invalid('%s: %s' % (toolkit._('User not found'),
                                              user_name))
    return ','.join(user_names)


def users_in_org_exists(key, data, errors, context):
    users = data.get(key).split(',')
    owner_org = data.get(('owner_org',))
    org = toolkit.get_action('organization_show')({}, {'id': owner_org})
    org_name = org.get('name')
    org_users = org.get('users')
    org_users = [user.get('name') for user in org_users]

    for user in users:
        if user in org_users:
            message = 'User {0} is already a member of the organization {1}.'\
                .format(user, org_name)
            raise toolkit.Invalid(message)
