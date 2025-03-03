from odoo import models, fields, api


class LichLamViec(models.Model):
    _name = 'lich_lam_viec'
    _description = 'Bảng chứa thông tin nhân viên'

    nhan_vien_id = fields.Many2one("nhan_vien", string= "Nhân Viên",required = True)
    ngay_lam = fields.Date("Ngày làm")