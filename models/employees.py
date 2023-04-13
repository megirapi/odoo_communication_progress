from odoo import fields, models, api


class ProjektiEmployees(models.Model):
    _name = 'projekti.employees'
    _description = 'Description'

    name = fields.Char(string=" Firstname/Lastname", required=True)
    gender = fields.Selection(string='Gender', required=False,
                              selection=[('f', 'Female'),
                                         ('m', 'Male'),
                                         ])
    cel = fields.Char(string='Cel', required=True)
    address = fields.Char(string='Address', required=False)
    salary = fields.Float(string='Salary',  required=True)
    emp_role = fields.Selection(string='Employee Role', required=False,
                                selection=[('front desk staff', 'Front Desk Staff'),
                                           ('housekeeping staff', 'Housekeeping Staff'),
                                           ('food and beverage staff', 'Food and Beverage Staff'),
                                           ('maintenance staff', 'Maintenance Staff'),
                                           ('accounting and finance staff', 'Accounting and Finance Staff'),
                                           ('human resources staff', 'Human Resources Staff'),
                                           ('security staff', 'Security Staff'),
                                           ('spa and wellness staff', 'Spa and Wellness Staff'),
                                           ('spa and wellness staff', 'Spa and Wellness Staff'),
                                           ])
    role_description = fields.Text(string="Role Description", required=False)
    shift_timing = fields.Selection(string='Shift Timing', required=False,
                                    selection=[('morning', 'Morning'),
                                               ('afternoon', 'Afternoon'),
                                               ('evening', 'Evening')])
    attendance = fields.Boolean(string='Attendance', default=False)
    attendance_count = fields.Integer(string='Attendance Count', default=0)
    punctuality = fields.Boolean(string='Punctuality', default=False)
    punctuality_count = fields.Integer(string='Punctuality Count', default=0)
    guest_satisfaction_rating = fields.Selection(string='Guest Satisfaction Rating', required=False,
                                                 selection=[('1', '1'),
                                                            ('2', '2'),
                                                            ('3', '3'),
                                                            ('4', '4'),
                                                            ('5', '5'),
                                                            ('6', '6'),
                                                            ('7', '7'),
                                                            ('8', '8'),
                                                            ('9', '9'),
                                                            ('10', '10')])
    total_hours_worked = fields.Float(string='Total Hours Worked', compute='_compute_total_hours_worked')
    overall_rating = fields.Float(string='Overall Rating', compute='_compute_overall_rating', store=True)
    bonus = fields.Float(string='Bonus', compute='_compute_bonus', store=True)

    @api.onchange('attendance')
    def update_attendance_count(self):
        if self.attendance:
            self.attendance_count += 1
        print("Attendance count updated:", self.attendance_count)

    @api.onchange('punctuality')
    def update_punctuality_count(self):
        if self.punctuality:
            self.punctuality_count += 1

    @api.depends('attendance_count', 'shift_timing')
    def _compute_total_hours_worked(self):
        for employee in self:
            if employee.attendance_count and employee.shift_timing:
                if employee.shift_timing == 'morning':
                    total_hours = employee.attendance_count * 8  # shift is 8 hours
                elif employee.shift_timing == 'afternoon':
                    total_hours = employee.attendance_count * 8  # shift is 6 hours
                elif employee.shift_timing == 'evening':
                    total_hours = employee.attendance_count * 10  # shift is 8 hours
                employee.total_hours_worked = total_hours
            else:
                employee.total_hours_worked = 0.0

    @api.depends('attendance_count', 'punctuality_count', 'guest_satisfaction_rating')
    def _compute_overall_rating(self):
        for employee in self:
            total_attendance_count = employee.attendance_count
            total_punctuality_count = employee.punctuality_count
            total_guest_satisfaction_rating = int(employee.guest_satisfaction_rating)
            overall_rating = (total_attendance_count + total_punctuality_count + total_guest_satisfaction_rating) / 3
            employee.overall_rating = overall_rating

    @api.depends('overall_rating')
    def _compute_bonus(self):
        for employee in self:
            if employee.overall_rating >= 9:
                employee.bonus = employee.salary * 0.2
            elif employee.overall_rating >= 8:
                employee.bonus = employee.salary * 0.1
            elif employee.overall_rating >= 7:
                employee.bonus = employee.salary * 0.05
            else:
                employee.bonus = 0.0
            employee.bonus = round(employee.bonus, 2)

