from odoo import models, fields, api
from datetime import date


class QuyTrinhDaoTao(models.Model):
    _name = 'quy_trinh_dao_tao'
    _description = 'Bảng chứa thông tin quy trình đào tạo'

    ma_khoa_dao_tao = fields.Char("Mã khóa đào tạo", required=True)
    ten_khoa_dao_tao = fields.Char("Tên khóa đào tạo", required=True)
    noi_dung_dao_tao = fields.Char("Nội dung đào tạo")
    ngay_bat_dau = fields.Date(string="Ngày Bắt Đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày kết thúc", required=True)  
    thoi_gian_dao_tao = fields.Integer(string="Thời gian đào tạo (ngày)", compute="_compute_thoi_gian_dao_tao", store=True)


    @api.depends('ngay_bat_dau', 'ngay_ket_thuc')
    def _compute_thoi_gian_dao_tao(self):
        for record in self:
            if record.ngay_bat_dau and record.ngay_ket_thuc:
                record.thoi_gian_dao_tao = (record.ngay_ket_thuc - record.ngay_bat_dau).days
            else:
                record.thoi_gian_dao_tao = 0