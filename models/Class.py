import datetime
from datetime import timedelta
from odoo import fields, models, api, _
from odoo.tools import format_datetime


class ClassData(models.Model):
    _name = 'class.data'
    _rec_name = 'std'
    std = fields.Selection(
        [('1st', '1st'), ('2nd', '2nd'), ('3rd', '3rd'), ('4th', '4th'), ('5th', '5th'), ('6th', '6th'), ('7th', '7th'),
         ('8th', '8th'), ('9th', '9th'), ('10th', '10th'), ('11th', '11th'), ('12th', '12th')], string='Standard',
        required=True)
    tot_stu = fields.Integer(string='Total students', required=True)
    pre_stu = fields.Integer(string='Present students', required=True)
    date = fields.Datetime('Time')
    student_ids = fields.One2many(string='students', comodel_name='student.data', inverse_name='class_id')
    teacher_id = fields.Many2many(string='teacher', comodel_name='teacher.data')

    entry_time = fields.Datetime('Entry Time')
    exit_time = fields.Datetime('Exit Time', compute='auto_time_set', store=True)

    @api.depends('entry_time')
    def auto_time_set(self):
        if self.entry_time:
            self.exit_time = self.entry_time + timedelta(hours=5)

    @api.model
    def create(self, vals_list):
        print(vals_list)
        return super(ClassData, self).create(vals_list)

    def write(self, vals):
        vals = {'name': 'a'}
        res = super(ClassData, self).write(vals)
        if res:
            print('true')
            return res
        else:
            print('False')
            return False


class TimeSheet(models.Model):
    _name = 'time.sheet'
    _rec_name = 'stud_id'

    stud_id = fields.Char('Student id')
    # stud_name = fields.Char('name')
    check_in = fields.Datetime('Entry Time')
    check_out = fields.Datetime('Exit Time')
    time_spend = fields.Float('Total Time Spent')
    class_name = fields.Char('standard')
    # class_entry_time = fields.Datetime('Class Entry Time', related='class_name.entry_time')
    # class_exit_time = fields.Datetime('Class Exit Time', related='class_name.exit_time')

    message = fields.Char('message')

    # def name_get(self):
    #     result = []
    #     for attendance in self:
    #         if not attendance.check_out:
    #             result.append((attendance.id, _("%(empl_name)s from %(check_in)s") % {
    #                 'empl_name': attendance.stud_name.name,
    #                 'check_in': format_datetime(self.env, attendance.check_in, dt_format=False),
    #             }))
    #         else:
    #             result.append((attendance.id, _("%(empl_name)s from %(check_in)s to %(check_out)s") % {
    #                 'empl_name': attendance.stud_name.name,
    #                 'check_in': format_datetime(self.env, attendance.check_in, dt_format=False),
    #                 'check_out': format_datetime(self.env, attendance.check_out, dt_format=False),
    #             }))
    #     return result

    @api.onchange('check_in', 'check_out')
    def time_spent(self):
        if self.check_out:
            if self.check_out > self.check_in:
                self.time_spend = self.check_out - self.check_in

        #     elif self.check_out > self.class_exit_time:
        #         student_exit_time = self.check_out - self.class_exit_time
        #         self.message = f'You are going {student_exit_time} Hours early today! good bye'
        #
        #     elif self.check_out < self.class_exit_time:
        #         student_exit_time = self.class_exit_time - self.check_out
        #         self.message = f'You are going {student_exit_time} Hours late today! good bye'
        #
        # if self.check_in > self.class_entry_time:
        #     student_entry_time = self.check_in - self.class_entry_time
        #     self.message = f'Welcome, you are {student_entry_time} Hours late today'
        #
        # elif self.check_in < self.class_entry_time:
        #     student_entry_time = self.class_entry_time - self.check_in
        #     self.message = f'Welcome, you are {student_entry_time} Hours early today'

        else:
            self.message = 'congratulations you are on time'
