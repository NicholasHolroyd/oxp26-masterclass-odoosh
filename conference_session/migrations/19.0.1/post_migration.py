from odoo.upgrade import util


def _column_exists(cr, table, column):
    cr.execute("""
        SELECT 1 FROM information_schema.columns
        WHERE table_name = %s AND column_name = %s
    """, (table, column))
    return cr.fetchone() is not None


def migrate(cr, version):
    # presenter_id now exists (added by the ORM). Copy over what
    # pre_migration resolved from the old speaker names, then drop the
    # scratch column.
    cr.execute("""
        UPDATE conference_session
        SET presenter_id = _migrate_presenter_id
        WHERE _migrate_presenter_id IS NOT NULL
    """)
    cr.execute("ALTER TABLE conference_session DROP COLUMN _migrate_presenter_id")

    # speaker was already read in pre_migration; only clean it up here if it
    # is still around (defensive against a partial/previous run).
    if _column_exists(cr, 'conference_session', 'speaker'):
        util.remove_field(cr, 'conference.session', 'speaker')

    # duration_in_hours is now redundant: 'duration' is stored in hours directly.
    if _column_exists(cr, 'conference_session', 'duration_in_hours'):
        util.remove_field(cr, 'conference.session', 'duration_in_hours')
