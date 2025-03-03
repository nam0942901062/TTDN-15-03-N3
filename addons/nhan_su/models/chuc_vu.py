from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'chuc_vu'
    _description = 'Bảng chứa thông tin chức vụ'
    _rec_name = "ten_chuc_vu"

    ma_chuc_vu = fields.Char("Mã chức vụ", required=True)
    ten_chuc_vu = fields.Char("Tên chức vụ", required=True)
    quyen_han = fields.Char("Quyền hạn")
    mo_ta = fields.Char("Mô tả")
    nhan_vien_id = fields.One2many("nhan_vien", inverse_name = 'chuc_vu_id', string= "Nhân Viên")
    
    @api.onchange("ten_chuc_vu")
    def _tinh_thay_doi(self):
       for record in self:
           if record.ten_chuc_vu:
                record.ma_chuc_vu = record.ten_chuc_vu