def migrate(cr, version):
    # duration: Integer (minutes) -> Float (hours), converted before the ORM
    # touches the column so no data is lost or naively re-cast.
    cr.execute("""
        ALTER TABLE conference_session
        ALTER COLUMN duration TYPE float
        USING ROUND(duration::numeric / 60, 2)
    """)
    # NOTE: 'speaker' is left untouched here — post_migration reads it to
    # find or create the matching res.partner records.
