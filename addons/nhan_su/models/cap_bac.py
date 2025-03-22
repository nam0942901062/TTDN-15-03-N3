from odoo import models, fields, api


class ChucVu(models.Model):
    _name = 'cap_bac'
    _description = 'Bảng chứa thông tin chức vụ'
    _rec_name = "ten_cap_bac"

    ma_cap_bac = fields.Char("Mã cấp bậc", required=True)
    ten_cap_bac = fields.Char("Tên cấp bậc", required=True)
    quyen_han = fields.Char("Quyền hạn")
    mo_ta = fields.Char("Mô tả")
    nhan_vien_id = fields.One2many("nhan_vien", inverse_name = 'cap_bac_id', string= "Nhân Viên")
    so_luong_nhan_vien = fields.Integer(string="Số lượng nhân viên", compute="_compute_so_luong_nhan_vien", store=True)
    
    
    @api.depends('nhan_vien_id')
    def _compute_so_luong_nhan_vien(self):
        for record in self:
            record.so_luong_nhan_vien = len(record.nhan_vien_id)
    
    @api.onchange("ten_cap_bac")
    def _tinh_thay_doi(self):
       for record in self:
           if record.ten_cap_bac:
                record.ma_cap_bac = record.ten_cap_bac