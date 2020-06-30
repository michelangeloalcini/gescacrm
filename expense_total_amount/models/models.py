from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools import email_split, float_is_zero

from odoo.addons import decimal_precision as dp

class Expense(models.Model):
    _inherit = 'hr.expense'
    
    total_amount = fields.Monetary("Total", compute='_compute_total_amount', store=True, currency_field='currency_id', digits=dp.get_precision('Account'))
    
    @api.depends('quantity', 'unit_amount', 'tax_ids', 'currency_id', 'x_studio_km_casa_lavoro','product_uom_id')
    def _compute_total_amount(self):
        for expense in self:
            if expense.product_uom_id.display_name == 'km':
                expense.untaxed_amount = expense.unit_amount * (expense.quantity - expense.x_studio_km_casa_lavoro)
                taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.quantity - expense.x_studio_km_casa_lavoro, expense.product_id, expense.employee_id.user_id.partner_id)
                expense.total_amount = taxes.get('total_included')
            else:
                expense.untaxed_amount = expense.unit_amount * expense.quantity
                taxes = expense.tax_ids.compute_all(expense.unit_amount, expense.currency_id, expense.quantity, expense.product_id, expense.employee_id.user_id.partner_id)
                expense.total_amount = taxes.get('total_included')