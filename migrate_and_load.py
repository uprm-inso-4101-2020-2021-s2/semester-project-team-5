import os
import shutil

from django.conf import settings
from django.core.management import execute_from_command_line
from django.db import connection

if __name__ == "__main__":

    # Gather all app names
    app_names = []
    apps_sql_condition = "tablename LIKE 'django%' "
    for app in settings.INSTALLED_APPS:
        app_names.append(app.rsplit('.', 1)[-1])

    # Remove migration directories and prepare to drop all tables
    for app_name in app_names:
        app_migration_dir = '%s\\%s\\migrations' % (settings.BASE_DIR, app_name)
        if os.path.exists(app_migration_dir):
            shutil.rmtree(app_migration_dir)
        apps_sql_condition += " OR tablename LIKE '%s%%'" % app_name

    # Make migrations
    args = ['manage.py', 'makemigrations', ] + app_names
    execute_from_command_line(args)

    # Copy DB extensions migration step
    # shutil.copy(os.path.join(settings.BASE_DIR, "0002_DBExtensions.py"),
    #             os.path.join(settings.BASE_DIR, "items", "migrations", "0002_DBExtensions.py"))

    # Drop all tables from DB
    cursor = connection.cursor()
    all_tabls_sql = ('SELECT pg_tables.tablename FROM pg_tables WHERE %s' % apps_sql_condition) + ';'
    cursor.execute(all_tabls_sql)
    all_tables = cursor.fetchall()
    sql = '\n'.join('DROP TABLE IF EXISTS public.\"%s\" CASCADE;' % table for (table,) in all_tables)
    if len(sql.lstrip()) > 0:
        connection.cursor().execute(sql)

    # Migrate DB
    execute_from_command_line(['manage.py', 'migrate', ])

    # Import initial data
    # execute_from_command_line(['manage.py', 'loaddata', os.path.join(settings.BASE_DIR, 'initial_data.json'), ])

    exit(0)
