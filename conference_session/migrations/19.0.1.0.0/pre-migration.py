from odoo.upgrade import util

def migrate(cr, version):
    # duration: Integer (minutes) → Float (hours), before ORM touches the column
    cr.execute("""
        ALTER TABLE conference_session
        ALTER COLUMN duration TYPE float
        USING ROUND(duration::numeric / 60, 2)
    """)
    # NOTE: 'speaker' is left untouched here — post_migration reads it to create partners
