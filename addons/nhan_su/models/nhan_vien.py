from odoo import models, fields, api
from datetime import date
import re
from odoo.exceptions import ValidationError  # Import ValidationError
from dateutil.relativedelta import relativedelta


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
    cap_bac_id = fields.Many2one("cap_bac", inverse_name = 'nhan_vien_id',string="Cấp bậc")
    phong_ban_id = fields.Many2many('phong_ban', 'phong_ban_nhan_vien_rel', 
                                     'nhan_vien_id', 'phong_ban_id', string="Phòng Ban")
    la_truong_phong = fields.Boolean(string="Là Trưởng Phòng", compute="_compute_la_truong_phong", store=True)


    ho_ten_dem = fields.Char("Tên đệm")
    ten = fields.Char("Tên")
    so_dien_thoai = fields.Char("Số điện thoại", required = True)
    tuoi = fields.Integer("Tuổi",compute = '_tinh_tuoi', store = True)
    anh = fields.Binary("Ảnh")
    tinh_trang_hon_nhan = fields.Selection([
        ('doc_than', 'Độc thân'),
        ('da_ket_hon', 'Đã kết hôn'),
        ('khac', 'Khác'),
    ], string="Tình trạng hôn nhân", default='khac')
    gioi_tinh = fields.Selection([
        ('nam', 'Nam'),
        ('nu', 'Nữ'),
        ('khac', 'Khác'),
    ], string="Giới tính", default='khac', required=True)
    dia_chi = fields.Char("Địa Chỉ")
    so_ngan_hang = fields.Char(string="Số tài khoản ngân hàng", required=True)
    ten_ngan_hang = fields.Char(string="Tên sở hữu", required=True)
    ngan_hang = fields.Char(string="Tên ngân hàng", required=True)
    
    
    quoc_tich = fields.Char("Quốc tịch", required=True)
    nick_name = fields.Char("Nick name")
    ho_khau = fields.Char("Hộ khẩu")
    cmnd = fields.Char("Chứng minh nhân dân", required=True)
    noi_cap = fields.Char("Nơi cấp", required=True)
    facebook = fields.Char("Facebook")
    email_2 = fields.Char("email khác")
    
    
    luu_file_id = fields.One2many('luu_file',inverse_name = 'nhan_vien_id', string="Lưu file")
    
    
    bang_cap = fields.Selection([
        ('daihoc', 'Đại Học'),
        ('caoddang', 'Cao Đẳng'),
        ('trungcap', 'Trung Cấp'),
        ('khac', 'Khác'),
    ], string="Bằng Cấp")
    ngay_bat_dau_hoc = fields.Date("Ngày Bắt Đầu Học")
    ngay_ket_thuc_hoc = fields.Date("Ngày Kết Thúc Học")
    ghi_chu_bang_cap = fields.Char("Ghi chú Bằng Cấp", help="Nhập chi tiết bằng cấp nếu chọn 'Khác'")
    truong_hoc = fields.Char("Tên trường học")
    
    
    ten_hop_dong = fields.Char(string="Tên Hợp Đồng", required=True)
    luong = fields.Monetary(string="Lương", required=True, currency_field="currency_id")
    ngay_bat_dau = fields.Date(string="Ngày Bắt Đầu", required=True)
    ngay_ket_thuc = fields.Date(string="Ngày Kết Thúc")
    trang_thai = fields.Selection([
        ('draft', 'Nháp'),
        ('running', 'Đang Hoạt Động'),
        ('expired', 'Hết Hạn'),
    ], string="Trạng Thái", compute="_compute_state", store=True)
    currency_id = fields.Many2one(
        "res.currency", string="Đơn vị tiền tệ", default=lambda self: self.env.company.currency_id
    )
    tham_nien = fields.Float(string="Thâm niên (năm)", compute="_compute_tham_nien", store=True)

    @api.depends('ngay_bat_dau', 'trang_thai')
    def _compute_tham_nien(self):
        """Tính số năm thâm niên dựa trên ngày bắt đầu và chỉ tính nếu hợp đồng đang hoạt động"""
        today = date.today()
        for nhan_vien in self:
            if nhan_vien.trang_thai == 'running' and nhan_vien.ngay_bat_dau:
                delta = relativedelta(today, nhan_vien.ngay_bat_dau)
                nhan_vien.tham_nien = round(delta.years + delta.months / 12, 2)  # Tính năm, làm tròn 2 số thập phân
            else:
                nhan_vien.tham_nien = 0  # Nếu không có hợp đồng đang chạy, thâm niên = 0
    
    # color = fields.Integer("Màu sắc", compute="_compute_color", store=True)
    
    
    

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



    # @api.depends("trang_thai")
    # def _compute_color(self):
    #     for rec in self:
    #         if rec.trang_thai == 'draft':
    #             rec.color = 4  # Xám
    #         elif rec.trang_thai == 'running':
    #             rec.color = 10  # Xanh lá
    #         elif rec.trang_thai == 'expired':
    #             rec.color = 1  # Đỏ
    
    
    @api.constrains('ngay_bat_dau_hoc', 'ngay_ket_thuc_hoc')
    def _check_thoi_gian_hoc(self):
        for rec in self:
            if rec.ngay_bat_dau_hoc and rec.ngay_ket_thuc_hoc and rec.ngay_bat_dau_hoc > rec.ngay_ket_thuc_hoc:
                raise models.ValidationError("Ngày bắt đầu không được lớn hơn ngày kết thúc!")
            
    @api.depends('chuc_vu_id')
    def _compute_la_truong_phong(self):
        """Xác định nhân viên có phải Trưởng Phòng không."""
        for rec in self:
            rec.la_truong_phong = rec.chuc_vu_id.ten_chuc_vu == "Trưởng Phòng"

    @api.constrains('phong_ban_id')
    def _check_truong_phong(self):
        """Đảm bảo một nhân viên không thể làm Trưởng Phòng ở nhiều nơi."""
        for rec in self:
            if rec.la_truong_phong and rec.phong_ban_id:
                existing = self.env['phong_ban'].search([
                    ('truong_phong_id', '=', rec.id),
                    ('id', '!=', rec.phong_ban_id.id)
                ])
                if existing:
                    raise ValidationError(f"{rec.ten_nhan_vien} đã là Trưởng Phòng của {existing.ten_phong_ban}!")