def migrate(cr, version):
    # duration: Integer (minutes) -> Float (hours), converted before the ORM
    # touches the column so no data is lost or naively re-cast.
    cr.execute("""
        ALTER TABLE conference_session
        ALTER COLUMN duration TYPE float
        USING ROUND(duration::numeric / 60, 2)
    """)

    # speaker -> presenter_id: resolve it now, while the column still exists.
    # presenter_id isn't created yet at this point (the ORM adds it after
    # pre-migrate runs), so stash the resolved partner per session in a
    # scratch column and let post_migration copy it across once presenter_id
    # exists.
    cr.execute("ALTER TABLE conference_session ADD COLUMN _migrate_presenter_id integer")

    cr.execute("""
        SELECT id, speaker FROM conference_session
        WHERE speaker IS NOT NULL AND speaker != ''
    """)
    sessions = cr.fetchall()

    for session_id, speaker_name in sessions:
        cr.execute(
            "SELECT id FROM res_partner WHERE name = %s AND active = true LIMIT 1",
            (speaker_name,),
        )
        row = cr.fetchone()
        if row:
            partner_id = row[0]
        else:
            cr.execute(
                "INSERT INTO res_partner (name, active, company_type) VALUES (%s, true, 'person') RETURNING id",
                (speaker_name,),
            )
            partner_id = cr.fetchone()[0]

        cr.execute(
            "UPDATE conference_session SET _migrate_presenter_id = %s WHERE id = %s",
            (partner_id, session_id),
        )
