from odoo.upgrade import util

def migrate(cr, version):
    # ORM has run: presenter_id column exists (NULL), speaker column still has the old names
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
            "UPDATE conference_session SET presenter_id = %s WHERE id = %s",
            (partner_id, session_id),
        )

    util.remove_field(cr, 'conference.session', 'speaker')
