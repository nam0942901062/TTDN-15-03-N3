from odoo import models, fields, api


class PhongBan(models.Model):
    _name = 'phong_ban'
    _description = 'Bảng chứa thông tin phòng ban'
    _rec_name = "ten_phong_ban"

    ma_phong_ban = fields.Char("Mã phòng ban", required=True)
    ten_phong_ban = fields.Char("Tên phòng ban", required=True)
    nhan_vien_id = fields.Many2many('nhan_vien', 'phong_ban_nhan_vien_rel', 
                                     'phong_ban_id', 'nhan_vien_id', string="Danh sách nhân viên")
    so_luong_nhan_vien = fields.Integer(string="Số Lượng Nhân Viên", compute="_compute_so_luong_nhan_vien", store=True)
    truong_phong_id = fields.Many2one(
        'nhan_vien', 
        string="Trưởng Phòng",
        domain="[('chuc_vu_id.ten_chuc_vu', '=', 'Trưởng Phòng')]"
    )
    danh_sach_nhan_vien = fields.One2many('nhan_vien', 'phong_ban_id', string="Danh Sách Nhân Viên")
    # @api.depends('truong_phong_id')
    # def _compute_so_luong_truong_phong(self):
    #     for record in self:
    #         record.so_luong_truong_phong = len(record.truong_phong_id)


    @api.depends('nhan_vien_id')
    def _compute_so_luong_nhan_vien(self):
        for rec in self:
            rec.so_luong_nhan_vien = len(rec.nhan_vien_id)
    
            
    @api.onchange("ten_phong_ban")
    def _tinh_thay_doi(self):
       for record in self:
           if record.ten_phong_ban:
                record.ma_phong_ban = record.ten_phong_ban