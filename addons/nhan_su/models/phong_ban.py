from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = "ten_phong_ban"

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    truong_phong = fields.Char("Trưởng phòng")
    
    
    
    
    @api.onchange("ten_phong_ban")
    def _tinh_thay_doi(self):
       for record in self:
           if record.ten_phong_ban:
                record.ma_phong_ban = record.ten_phong_ban