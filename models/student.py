from datetime import datetime
from odoo import fields, models, api, _, exceptions


class StudentData(models.Model):
    _name = 'student.data'
    # _description = 'students data'
    _rec_name = 'stud_id'

    stud_id = fields.Char('id')
    name = fields.Char(string='name', required=True)
    age = fields.Integer(string='age', required=True)
    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ], string='gender')
    class_id = fields.Many2one(string='standard', comodel_name='class.data')
    s_entry = fields.Datetime('Enter your entry time')
    s_exit = fields.Datetime('Enter your exit time')
    total_hours = fields.Float('Total Hours')

    def error_raise(self):
        if 0 < self.age < 5:
            raise ValueError('please put age more than 5')

        if self.name and self.age and self.gender:
            raise ValueError('please fill all fields')
        else:
            pass

    def get_stud_results(self):
        return {
            'name': 'students result',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'students.result',
            'view_id': self.env.ref('school_management.add_results').id,
            'context': {'default_name': self.name},
            'target': 'new',
            'type': 'ir.actions.act_window',
        }

    def generate_id(self):
        self.stud_id = self.name + str(self.id)

    def unlink(self):
        return super(StudentData, self).unlink()

    def student_check_in(self):
        check_in = datetime.now()
        check_entry = self.env['time.sheet'].search([('stud_id', '=', self.stud_id)], limit=1).stud_id
        check_out = self.env['time.sheet'].search([('stud_id', '=', self.stud_id)], order='check_in desc', limit=1).check_out
        if check_out or not check_entry:
            self.env['time.sheet'].create({
                'stud_id': self.stud_id,
                'class_name': self.class_id.std,
                'check_in': check_in,
                'check_out': False,
                'time_spend': False,
            })

        else:
            raise exceptions.ValidationError(_('first check out'))

    def student_check_out(self):
        get_id = self.env['time.sheet'].search([('stud_id', '=', self.stud_id), ('check_out', '=', False)], limit=1)
        check_in = get_id.check_in
        if check_in:
            check_out = datetime.now()
            time_spend = (check_out - check_in).total_seconds() / 3600.0
            if not self.total_hours:
                self.total_hours = time_spend
            else:
                self.total_hours += time_spend
            get_id.write({
                'check_out': check_out,
                'time_spend': time_spend,
            })
            view = {
                'name': 'Students',
                'view_type': 'tree',
                "view_mode": "tree",
                "res_model": 'time.sheet',
                "type": "ir.actions.act_window",
                'target': 'new',
            }
            # {'value': {}, 'warning': {'title': 'warning', 'message': 'Your message'}}
        else:
            raise exceptions.ValidationError(_('first check in'))


class StudentsResult(models.Model):
    _inherit = 'student.data'

    teacher = fields.Char(string='Teacher')
    maths = fields.Char(string='Maths')
    science = fields.Char(string='Science')
    english = fields.Char(string='English')
    history = fields.Char(string='History')
    percentage = fields.Char(string='Percentage')


class CountTotal(models.Model):
    _inherit = 'sale.order'

    total = fields.Monetary('Total Money', compute='_compute_money')
    tax = fields.Monetary('Total Tax', compute='_compute_money')

    @api.onchange('partner_id')
    def _compute_money(self):
        total_data = [x.amount_total for x in self.env['sale.order'].search([('partner_id.name', '=', self.partner_id.name)])]
        total_amount_untaxed = [x.amount_untaxed for x in self.env['sale.order'].search([('partner_id.name', '=', self.partner_id.name)])]

        self.total = 0
        self.tax = 0
        amount_untaxed = 0
        for i in total_data:
            self.total += i

        for j in total_amount_untaxed:
            amount_untaxed += j
        self.tax = self.total - amount_untaxed
