from dataclasses import dataclass  # 导入 dataclass 装饰器
import xml.etree.ElementTree as ET  # 导入 ElementTree XML API
import re  # 导入正则表达式模块

@dataclass  # 使用 dataclass 装饰器定义数据类
class SatelliteImageData:
    entity_id: str  # 实体ID,用于唯一标识卫星图像
    acquisition_date: str  # 获取卫星图像的日期
    wrs_path: int  # WRS路径号,用于定位卫星图像在全球范围内的位置
    wrs_row: int  # WRS行号,用于定位卫星图像在全球范围内的位置
    wrs_type: str  # WRS类型,如1或2
    time_series: str  # 时间序列标识符
    datum: str  # 参考坐标系统
    zone_number: int  # 区带编号,用于UTM投影
    file_size: int  # 文件大小(字节)
    orientation: str  # 图像方向
    product_type: str  # 产品类型
    resampling_technique: str  # 重采样技术
    satellite_number: str  # 卫星编号
    sun_azimuth: float  # 太阳方位角(度)
    sun_elevation: float  # 太阳高度角(度)
    center_latitude: str  # 图像中心纬度(度分秒格式)
    center_longitude: str  # 图像中心经度(度分秒格式)
    nw_corner_lat: str  # 西北角纬度(度分秒格式)
    nw_corner_long: str  # 西北角经度(度分秒格式)
    ne_corner_lat: str  # 东北角纬度(度分秒格式)
    ne_corner_long: str  # 东北角经度(度分秒格式)
    se_corner_lat: str  # 东南角纬度(度分秒格式)
    se_corner_long: str  # 东南角经度(度分秒格式)
    sw_corner_lat: str  # 西南角纬度(度分秒格式)
    sw_corner_long: str  # 西南角经度(度分秒格式)
    center_latitude_dec: float  # 图像中心纬度(十进制度数)
    center_longitude_dec: float  # 图像中心经度(十进制度数)
    nw_corner_lat_dec: float  # 西北角纬度(十进制度数)
    nw_corner_long_dec: float  # 西北角经度(十进制度数)
    ne_corner_lat_dec: float  # 东北角纬度(十进制度数)
    ne_corner_long_dec: float  # 东北角经度(十进制度数)
    se_corner_lat_dec: float  # 东南角纬度(十进制度数)
    se_corner_long_dec: float  # 东南角经度(十进制度数)
    sw_corner_lat_dec: float  # 西南角纬度(十进制度数)
    sw_corner_long_dec: float  # 西南角经度(十进制度数)
    browse_link: str  # 浏览图像链接
    browse_thumbnail_link: str  # 浏览图像缩略图链接
    # overlay_link: str  # 叠加图像链接
    # overlay_thumbnail_link: str  # 叠加图像缩略图链接

    @classmethod  # 定义一个类方法
    def from_xml_file(cls, xml_file):
        tree = ET.parse(xml_file)  # 解析 XML 文件
        root = tree.getroot()  # 获取根元素
        nsmap = {'eemetadata': root.tag.split('}')[0][1:]}  # 从根元素标签中提取命名空间 URI

        # 解析 metadataFields 节点中的元数据字段
        metadata_fields = {
            field.attrib['name'].replace(' ', '_').lower(): field.find('eemetadata:metadataValue', nsmap).text
            for field in root.findall('eemetadata:metadataFields/eemetadata:metadataField', nsmap)
        }

        # 解析 browseLinks 节点中的链接
        browse_link = root.find('eemetadata:browseLinks/eemetadata:browse/eemetadata:browseLink', nsmap).text
        browse_thumbnail_link = root.find('eemetadata:browseLinks/eemetadata:browse', nsmap).attrib['thumbLink']

        # # 解析 overlayLinks 节点中的链接
        # overlay_link = root.find('eemetadata:overlayLinks/eemetadata:overlay/eemetadata:overlayLink', nsmap).text
        # overlay_thumbnail_link = root.find('eemetadata:overlayLinks/eemetadata:overlay', nsmap).attrib['thumbLink']

        # 创建并返回 SatelliteImageData 对象
        return cls(**{
            'entity_id': metadata_fields['entity_id'],
            'acquisition_date': metadata_fields['acquisition_date'],
            'wrs_path': int(metadata_fields['wrs_path']),
            'wrs_row': int(metadata_fields['wrs_row']),
            'wrs_type': metadata_fields['wrs_type'],
            'time_series': metadata_fields['time_series'],
            'datum': metadata_fields['datum'],
            'zone_number': int(metadata_fields['zone_number']),
            'file_size': int(metadata_fields['file_size']),
            'orientation': metadata_fields['orientation'],
            'product_type': metadata_fields['product_type'],
            'resampling_technique': metadata_fields['resampling_technique'],
            'satellite_number': metadata_fields['satellite_number'],
            'sun_azimuth': float(metadata_fields['sun_azimuth']),
            'sun_elevation': float(metadata_fields['sun_elevation']),
            'center_latitude': metadata_fields['center_latitude'],
            'center_longitude': metadata_fields['center_longitude'],
            'nw_corner_lat': metadata_fields['nw_corner_lat'],
            'nw_corner_long': metadata_fields['nw_corner_long'],
            'ne_corner_lat': metadata_fields['ne_corner_lat'],
            'ne_corner_long': metadata_fields['ne_corner_long'],
            'se_corner_lat': metadata_fields['se_corner_lat'],
            'se_corner_long': metadata_fields['se_corner_long'],
            'sw_corner_lat': metadata_fields['sw_corner_lat'],
            'sw_corner_long': metadata_fields['sw_corner_long'],
            'center_latitude_dec': cls.dms_to_decimal(metadata_fields['center_latitude']),
            'center_longitude_dec': cls.dms_to_decimal(metadata_fields['center_longitude']),
            'nw_corner_lat_dec': cls.dms_to_decimal(metadata_fields['nw_corner_lat']),
            'nw_corner_long_dec': cls.dms_to_decimal(metadata_fields['nw_corner_long']),
            'ne_corner_lat_dec': cls.dms_to_decimal(metadata_fields['ne_corner_lat']),
            'ne_corner_long_dec': cls.dms_to_decimal(metadata_fields['ne_corner_long']),
            'se_corner_lat_dec': cls.dms_to_decimal(metadata_fields['se_corner_lat']),
            'se_corner_long_dec': cls.dms_to_decimal(metadata_fields['se_corner_long']),
            'sw_corner_lat_dec': cls.dms_to_decimal(metadata_fields['sw_corner_lat']),
            'sw_corner_long_dec': cls.dms_to_decimal(metadata_fields['sw_corner_long']),
            'browse_link': browse_link,
            'browse_thumbnail_link': browse_thumbnail_link,
            # 'overlay_link': overlay_link,
            # 'overlay_thumbnail_link': overlay_thumbnail_link
        })

    @staticmethod  # 定义一个静态方法
    def dms_to_decimal(dms_str):
        """
        将度分秒格式的字符串转换为十进制浮点数
        """
        pattern = r"(-?\d+)&deg;\s*(\d+)'\s*(\d+\.\d+)\""  # 用于匹配度分秒字符串的正则表达式模式
        match = re.match(pattern, dms_str)  # 尝试匹配字符串
        if match:
            degrees = int(match.group(1))  # 提取度数
            minutes = int(match.group(2))  # 提取分钟
            seconds = float(match.group(3))  # 提取秒数
            decimal = degrees + (minutes / 60) + (seconds / 3600)  # 计算十进制值
            return decimal if dms_str.endswith('N') or dms_str.endswith('E') else -decimal  # 根据方向返回正负值
        else:
            raise ValueError(f"Invalid DMS string: {dms_str}")  # 如果无法匹配,抛出异常

# # 使用示例
# satellite_image_data = SatelliteImageData.from_xml_file("gls_all_LE70820552011359EDC00.xml")
# print(satellite_image_data)