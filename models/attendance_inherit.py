import datetime
from datetime import timedelta
from odoo import fields, models, api, _
import pytz


class EmployeeShift(models.Model):
    _name = 'shift.select'
    _rec_name = 'shift_name'
    shift_name = fields.Char('shift name')
    start_shift = fields.Float('start shift')
    end_shift = fields.Float('end shift')


class ShiftSelect(models.Model):
    _name = 'employee.shift'
    employee_name = fields.Many2one('hr.employee', 'Employee name')
    select_shift = fields.Many2one('shift.select', 'Select Shift')

    @api.onchange('employee_name')
    def distinct_name(self):
        for records in self:
            if self.env['employee.shift'].search([('employee_name', '=', records.employee_name.name)]):
                warning = {
                    'title': 'Warning',
                    'message': 'Name already exists'
                }
                records.employee_name = False
                return {'warning': warning}


class inherited_attendance_model(models.Model):
    _inherit = 'hr.attendance'
    check_in_early = fields.Float('early check in',  store=True)
    check_in_late = fields.Float('late check in',  store=True)
    check_out_early = fields.Float('early check out', store=True)
    check_out_late = fields.Float('late check out', store=True)

    @api.onchange('check_in', 'check_out')
    def checkin_checkout_time(self):
        IST = pytz.timezone('Asia/Kolkata')
        for records in self:
            start_shift = records.env['employee.shift'].search([('employee_name', '=', records.employee_id.name)]).select_shift.start_shift
            end_shift = records.env['employee.shift'].search([('employee_name', '=', records.employee_id.name)]).select_shift.end_shift
            if records.check_in and records.check_out:
                day_diff = records.check_in.astimezone(IST).date().day - records.check_in.astimezone(IST).date().day
                check_in = records.check_in.astimezone(IST).time().hour+records.check_in.astimezone(IST).time().minute*0.01+records.check_in.astimezone(IST).time().second*0.0001
                check_out = records.check_out.astimezone(IST).time().hour+records.check_out.astimezone(IST).time().minute*0.01+records.check_out.astimezone(IST).time().second*0.0001

                if start_shift and end_shift and day_diff == 0:
                    if check_in < start_shift:
                        records.check_in_early = (start_shift-0.4 - check_in)*100
                        records.check_in_late = 0

                    elif check_in > start_shift:
                        records.check_in_late = (check_in - start_shift)*100
                        records.check_in_early = 0

                    if check_out > end_shift:
                        records.check_out_late = (check_out - end_shift)*100
                        records.check_out_early = 0

                    elif check_out < end_shift:
                        records.check_out_early = (end_shift-0.4 - check_out)*100
                        records.check_out_late = 0

                elif records.check_in and records.check_out and start_shift and end_shift and day_diff > 0:
                    if check_in < start_shift:
                        records.check_in_early = (start_shift-0.4 - check_in + (day_diff * 24))*100
                        records.check_in_late = 0

                    elif check_in > start_shift:
                        records.check_in_late = (check_in - start_shift + (day_diff * 24))*100
                        records.check_in_early = 0

                    if check_out > end_shift:
                        records.check_out_late = (check_out - end_shift + (day_diff * 24))*100
                        records.check_out_early = 0

                    elif check_out < end_shift:
                        records.check_out_early = (end_shift-0.4 - check_out + (day_diff * 24))*100
                        records.check_out_late = 0

            elif records.check_in and start_shift:
                check_in = records.check_in.astimezone(IST).time().hour+records.check_in.astimezone(IST).time().minute*0.01

                if check_in < start_shift:
                    records.check_in_early = (start_shift-0.4 - check_in)*100
                    records.check_in_late = 0

                elif check_in > start_shift:
                    records.check_in_late = (check_in - start_shift)*100
                    records.check_in_early = 0

    # def early_late_in_out(self):
    #     for records in self:
    #         start_shift = records.env['employee.shift'].search([('employee_name', '=', records.employee_id.name)]).select_shift.start_shift
    #         end_shift = records.env['employee.shift'].search([('employee_name', '=', records.employee_id.name)]).select_shift.end_shift
    #         start_shift_dt = datetime.time(hour=int(start_shift), minute=(start_shift-int(start_shift))*100)
    #         end_shift_dt = datetime.time(hour=int(end_shift), minute=(end_shift-int(end_shift))*100)
    #         # if records.check_in:

    def late_attend_mail_cron_action(self):
        print('hello')
        body = [ids.id for ids in self.search([('check_in_late', '!=', False)])]
