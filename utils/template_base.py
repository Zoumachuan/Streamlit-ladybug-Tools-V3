# template_base.py

def map_value(value, old_min, old_max, new_min, new_max):
    """
    将值从一个范围映射到另一个范围。

    Args:
        value (float): 要映射的值。
        old_min (float): 旧范围的最小值。
        old_max (float): 旧范围的最大值。
        new_min (float): 新范围的最小值。
        new_max (float): 新范围的最大值。

    Returns:
        float: 映射后的值。
    """
    if old_max == old_min:
        return (new_max + new_min) / 2  # 防止除以零
    return ((value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min

# template_base.py

user_defined_colors = None

def set_user_defined_colors(color1, color2):
    """
    设置用户定义颜色。

    Args:
        color1 (str): 用户选择的第一个颜色（十六进制表示）。
        color2 (str): 用户选择的第二个颜色（十六进制表示）。
    """
    global user_defined_colors
    user_defined_colors = (hex_to_rgb(color1), hex_to_rgb(color2))

def hex_to_rgb(hex):
    """
    将十六进制颜色值转化为RGB元组。

    Args:
        hex (str): 十六进制颜色字符串（例如 "#FFFFFF"）。

    Returns:
        tuple: RGB元组。
    """
    hex = hex.lstrip('#')
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

# 其他现有代码...
def map_to_color(value, min_value, max_value, color_scheme):
    """
    将值映射到颜色。

    Args:
        value (float): 要映射的值。
        min_value (float): 值的最小值。
        max_value (float): 值的最大值。
        color_scheme (int): 色卡编号。

    Returns:
        str: 映射后的颜色（RGB格式）。
    """
    global user_defined_colors

    if color_scheme == 1:
        r = int(map_value(value, min_value, max_value, 0, 240))
        g = int(map_value(value, min_value, max_value, 0, 240))
        b = int(map_value(value, min_value, max_value, 0, 240))
    elif color_scheme == 2:
        # 冷色系颜色映射
        r = int(map_value(value, min_value, max_value, 65, 255))
        g = int(map_value(value, min_value, max_value, 65, 65))
        b = int(map_value(value, min_value, max_value, 255, 65))
    elif color_scheme == 3:
        # 红色到白色颜色映射
        r = int(map_value(value, min_value, max_value, 238, 255))
        g = int(map_value(value, min_value, max_value, 105, 245))
        b = int(map_value(value, min_value, max_value, 131, 228))
    elif color_scheme == 4:
        # 粉色到紫色颜色映射
        r = int(map_value(value, min_value, max_value, 151, 255))
        g = int(map_value(value, min_value, max_value, 92, 173))
        b = int(map_value(value, min_value, max_value, 141, 188))
    elif color_scheme == 5:
        # 蓝色到绿色颜色映射
        r = int(map_value(value, min_value, max_value, 34, 149))
        g = int(map_value(value, min_value, max_value, 87, 209))
        b = int(map_value(value, min_value, max_value, 126, 204))
    elif color_scheme == 6:
        # 黄色到橙色颜色映射
        r = int(map_value(value, min_value, max_value, 185, 117))
        g = int(map_value(value, min_value, max_value, 255, 121))
        b = int(map_value(value, min_value, max_value, 252, 231))
    elif color_scheme == 7:
        # 绿色到蓝色颜色映射
        r = int(map_value(value, min_value, max_value, 26, 229))
        g = int(map_value(value, min_value, max_value, 18, 229))
        b = int(map_value(value, min_value, max_value, 11, 203))
    elif color_scheme == 8:
        # 淡蓝色到蓝色颜色映射
        r = int(map_value(value, min_value, max_value, 109, 238))
        g = int(map_value(value, min_value, max_value, 159, 222))
        b = int(map_value(value, min_value, max_value, 217, 236))
    elif color_scheme == 9 and user_defined_colors is not None:
        # 用户自定义颜色映射
        r = int(map_value(value, min_value, max_value, user_defined_colors[0][0], user_defined_colors[1][0]))
        g = int(map_value(value, min_value, max_value, user_defined_colors[0][1], user_defined_colors[1][1]))
        b = int(map_value(value, min_value, max_value, user_defined_colors[0][2], user_defined_colors[1][2]))
    else:
        r, g, b = 0, 0, 0  # 默认黑色，如果色卡编号不在范围内

    return f'rgb({r}, {g}, {b})'

