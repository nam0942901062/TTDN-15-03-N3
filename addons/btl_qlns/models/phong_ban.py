from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)