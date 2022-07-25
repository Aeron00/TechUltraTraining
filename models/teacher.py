from odoo import fields, models, api


class TeacherData(models.Model):
    _name = 'teacher.data'

    name = fields.Char(string='name', required=True)
    age = fields.Integer(string='age', required=True)
    sub = fields.Selection([('maths', 'Maths'), ('science', 'Science'), ('english', 'English'), ('history', 'History')],
                           string='subject', required=True)
    gender = fields.Selection([
        ('male', 'Male'), ('female', 'Female'), ('other', 'Other')
    ], string='gender')
    class_ids = fields.Many2many(string='class', comodel_name='class.data')

    @api.model
    def create(self, vals_list):
        print(vals_list)
        return super(TeacherData, self).create(vals_list)

    def write(self, vals):
        print(vals)
        return super(TeacherData, self).write(vals)


class TeacherResult(models.Model):
    _name = 'teacher.result'

    name = fields.Many2one(string='students', comodel_name='student.data')
    class_name = fields.Many2one(string='Standard', comodel_name='class.data', related='name.class_id')
    # selection = []
    # name = fields.Selection(selection, 'students')
    teacher = fields.Many2many(string='Teacher', comodel_name='teacher.data')
    maths = fields.Integer(string='Maths')
    science = fields.Integer(string='Science')
    english = fields.Integer(string='English')
    history = fields.Integer(string='History')
    total = fields.Integer(string='Total')
    percentage = fields.Float(string='Percentage')

    def count_perc(self):
        total = self.maths + self.science + self.english + self.history
        self.percentage = total / 4

    def stud_copy(self):
        data = {
            'teacher': [x.name for x in self.teacher],
            'maths': self.maths,
            'science': self.science,
            'english': self.english,
            'history': self.history,
            'percentage': self.percentage,
        }
        self.env['student.data'].search([('stud_id', '=', self.name.stud_id)]).write(data)

    # @api.onchange('class_name')
    # def student_names(self):
    #     names = self.env['student.data'].search([('class_id', '=', self.class_name.std)])
    #     for name in names:
    #         self.selection.append((name.name, name.name))
    #     self.name = fields.Selection(self.selection, 'students')

# @api.v8
