from odoo import models, fields

class LuuFile(models.Model):
    _name = 'luu_file'
    _description = 'Lưu file'

    nhan_vien_id = fields.Many2one('nhan_vien', inverse_name = 'luu_file_id', string="Nhân Viên", ondelete="cascade")
    luu_file = fields.Binary("Tệp", attachment=True)  # Trường lưu file
    luu_file_name = fields.Char("Tên Tệp")  # Để lưu tên file