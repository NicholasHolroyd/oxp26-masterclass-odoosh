from odoo.tests.common import TransactionCase


class TestConferenceSession(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Session = cls.env['conference.session']
        cls.presenter = cls.env['res.partner'].create({'name': 'Test Presenter'})

    def test_duration_stored_in_hours(self):
        """Duration is stored directly in hours as a float."""
        session = self.Session.create({'name': 'Short Talk', 'duration': 0.5})
        self.assertAlmostEqual(session.duration, 0.5)

    def test_duration_accepts_fractional_hours(self):
        """A duration like 1h30 is stored as 1.5."""
        session = self.Session.create({'name': 'Long Session', 'duration': 1.5})
        self.assertAlmostEqual(session.duration, 1.5)

    def test_duration_defaults_to_zero(self):
        """No duration set → 0.0 hours."""
        session = self.Session.create({'name': 'TBD'})
        self.assertAlmostEqual(session.duration, 0.0)

    def test_presenter_id_links_to_partner(self):
        """presenter_id points to a res.partner record."""
        session = self.Session.create({
            'name': 'Keynote',
            'presenter_id': self.presenter.id,
        })
        self.assertEqual(session.presenter_id, self.presenter)

    def test_presenter_id_optional(self):
        """A session can be created without a presenter."""
        session = self.Session.create({'name': 'Workshop'})
        self.assertFalse(session.presenter_id)
