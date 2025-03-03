from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError  # Import ValidationError


class NhanVien(models.Model):
    _name = 'nhan_vien'
    _description = 'Bảng chứa thông tin nhân viên'
    _rec_name = 'ho_ten'
    # _sql_constrains = [
    #     ('ma_dinh_danh', 'unique(ma_dinh_danh)', 'Mã định danh phải là duy nhất')
    #     ]

    ma_dinh_danh = fields.Char("Mã định danh", required=True)
    ngay_sinh = fields.Date("Ngày sinh")
    que_quan = fields.Char("Quê quán")
    email = fields.Char("Email")
    so_dien_thoai = fields.Char("Số điện thoại")
    ho_ten = fields.Char("Họ và tên", compute ='_tinh_ho_ten', store=True)
    lich_lam_viec_id = fields.One2many("lich_lam_viec", inverse_name = 'nhan_vien_id',string="Danh sách lịch sử làm việc")
    chuc_vu_id = fields.Many2one("chuc_vu", inverse_name = 'nhan_vien_id',string="Chức vụ")
    ho_ten_dem = fields.Char("Tên đệm")
    ten = fields.Char("Tên")
    so_dien_thoai = fields.Char("Số điện thoại", required = True)
    tuoi = fields.Integer("Tuổi",compute = '_tinh_tuoi', store = True)
    anh = fields.Binary("Ảnh")
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('gay', 'Gay'),
    ], string="Giới tính", default='gay', required=True)
    
    ten_hop_dong = fields.Char(string="Tên Hợp Đồng", required=True)
    luong = fields.Monetary(string="Lương", required=True, currency_field="currency_id")
    ngay_bat_dau = fields.Date(string="Ngày Bắt Đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày Kết Thúc")
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('running', 'Đang Hoạt Động'),
        ('expired', 'Hết Hạn'),
    ], string="Trạng Thái", compute="_compute_state", store=True)
    currency_id = fields.Many2one('res.currency', string="Currency", default=lambda self: self.env.ref('base.VND').id)
    
    
    
    
    

    @api.depends('ngay_ket_thuc')
    def _compute_state(self):
        """Tự động cập nhật trạng thái hợp đồng"""
        today = fields.Date.today()
        for nhan_vien in self:
            if nhan_vien.ngay_ket_thuc and nhan_vien.ngay_ket_thuc < today:
                nhan_vien.trang_thai = 'expired'
            elif nhan_vien.ngay_bat_dau and nhan_vien.ngay_bat_dau <= today:
                nhan_vien.trang_thai = 'running'
            else:
                nhan_vien.trang_thai = 'draft'
     
    @api.depends("ho_ten_dem","ten")
    def _tinh_ho_ten(self):
        for record in self:
            if record.ho_ten_dem and record.ten:
                record.ho_ten = record.ho_ten_dem + ' ' + record.ten
                
    # @api.onchange("ho_ten_dem", "ten")
    # def _tinh_thay_doi(self):
    #     for record in self:
    #         if record.ho_ten_dem and record.ten:
    #             record.ma_dinh_danh = record.ten
    
    @api.depends("ngay_sinh")
    def _tinh_tuoi(self):
        today = date.today()
        for record in self:
            if record.ngay_sinh:
                sinh_ngay = record.ngay_sinh  # Kiểu datetime.date
                record.tuoi = today.year - sinh_ngay.year - (
                    (today.month, today.day) < (sinh_ngay.month, sinh_ngay.day)
                )
            else:
                record.tuoi = 0 
                
    @api.constrains('so_dien_thoai')
    def _check_phone_number(self):
        for record in self:
            if record.so_dien_thoai:
                # Kiểm tra số điện thoại phải có đúng 10 số và bắt đầu bằng '0'
                if not re.fullmatch(r'0\d{9}', record.so_dien_thoai):
                    raise ValidationError("⚠ Số điện thoại không hợp lệ (Bắt đầu từ 0 và có 10 số)")
                
    @api.depends('luong')
    def _tinh_luong(self):
        for rec in self:
            rec.luong = rec.luong if isinstance(rec.luong, (int, float)) else 0.0
