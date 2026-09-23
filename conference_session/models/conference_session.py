from odoo import fields, models,api


class ConferenceSession(models.Model):
    _name = 'conference.session'
    _description = 'Conference Session'
    _order = 'date, name'

    name = fields.Char(string='Title', required=True)
    presenter_id = fields.Many2one('res.partner', string='Presenter')
    duration = fields.Float(string='Duration (hours)')
    room = fields.Char(string='Room')
    notes = fields.Text(string='Notes')
    date = fields.Date(string='Date')

    @api.depends('duration')
    def _compute_duration_in_hours(self):
        for session in self:
            session.duration_in_hours = session.duration / 60.0
