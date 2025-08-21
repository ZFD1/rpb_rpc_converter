#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
RPB/RPC文件格式转换工具

该工具用于实现rpb和rpc文件格式的相互转换。
根据输入文件的扩展名自动执行反向转换。
"""

import os
import sys
import logging
import argparse
from pathlib import Path

# 配置日志记录
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def validate_input(input_file, output_dir):
    """
    验证输入文件和输出目录
    
    Args:
        input_file (str): 输入文件路径
        output_dir (str): 输出目录路径
        
    Returns:
        bool: 验证是否通过
    """
    # 检查输入文件是否存在
    if not os.path.isfile(input_file):
        logger.error(f"输入文件不存在: {input_file}")
        return False
    
    # 检查文件扩展名是否为.rpb或.rpc
    file_ext = os.path.splitext(input_file)[1].lower()
    if file_ext not in [".rpb", ".rpc"]:
        logger.error(f"不支持的文件格式: {file_ext}，仅支持.rpb和.rpc格式")
        return False
    
    # 检查输出目录是否存在，如果不存在则创建
    if not os.path.exists(output_dir):
        try:
            os.makedirs(output_dir)
            logger.info(f"已创建输出目录: {output_dir}")
        except OSError as e:
            logger.error(f"无法创建输出目录: {output_dir}, 错误: {e}")
            return False
    
    # 检查输出目录是否可写
    if not os.access(output_dir, os.W_OK):
        logger.error(f"输出目录不可写: {output_dir}")
        return False
    
    return True


def parse_rpb_file(input_file):
    """
    解析RPB文件，提取RPC参数
    
    Args:
        input_file (str): 输入RPB文件路径
        
    Returns:
        dict: 包含RPC参数的字典
    """
    try:
        # 初始化参数字典
        params = {}
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        # 提取偏移量和比例参数
        params['lineOffset'] = extract_value(content, 'lineOffset')
        params['sampOffset'] = extract_value(content, 'sampOffset')
        params['latOffset'] = extract_value(content, 'latOffset')
        params['longOffset'] = extract_value(content, 'longOffset')
        params['heightOffset'] = extract_value(content, 'heightOffset')
        params['lineScale'] = extract_value(content, 'lineScale')
        params['sampScale'] = extract_value(content, 'sampScale')
        params['latScale'] = extract_value(content, 'latScale')
        params['longScale'] = extract_value(content, 'longScale')
        params['heightScale'] = extract_value(content, 'heightScale')
        
        # 提取系数参数
        params['lineNumCoef'] = extract_array(content, 'lineNumCoef')
        params['lineDenCoef'] = extract_array(content, 'lineDenCoef')
        params['sampNumCoef'] = extract_array(content, 'sampNumCoef')
        params['sampDenCoef'] = extract_array(content, 'sampDenCoef')
        
        return params
    except Exception as e:
        logger.error(f"解析RPB文件失败: {e}")
        raise


def extract_value(content, key):
    """
    从RPB文件内容中提取单个值
    
    Args:
        content (str): 文件内容
        key (str): 要提取的键名
        
    Returns:
        str: 提取的值
    """
    import re
    pattern = f"{key}\s*=\s*([+-]?\d+\.\d+e[+-]\d+|[+-]?\d+\.\d+|[+-]?\d+)"
    match = re.search(pattern, content)
    if match:
        return match.group(1)
    return None


def extract_array(content, key):
    """
    从RPB文件内容中提取数组值
    
    Args:
        content (str): 文件内容
        key (str): 要提取的键名
        
    Returns:
        list: 提取的数组值
    """
    import re
    pattern = f"{key}\s*=\s*\(([^\)]+)\)"
    match = re.search(pattern, content)
    if match:
        values_str = match.group(1)
        # 移除所有空白字符并按逗号分割
        values = [v.strip() for v in values_str.split(',') if v.strip()]
        return values
    return []


def parse_rpc_file(input_file):
    """
    解析RPC文件，提取RPC参数
    
    Args:
        input_file (str): 输入RPC文件路径
        
    Returns:
        dict: 包含RPC参数的字典
    """
    try:
        # 初始化参数字典
        params = {}
        
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # 解析RPC文件中的参数
        for line in lines:
            line = line.strip()
            if ':' in line:
                key, value = line.split(':', 1)
                key = key.strip()
                value = value.strip().split()[0]  # 取第一个值，忽略单位
                
                # 映射RPC文件中的键到RPB文件中的键
                if key == 'LINE_OFF':
                    params['lineOffset'] = value
                elif key == 'SAMP_OFF':
                    params['sampOffset'] = value
                elif key == 'LAT_OFF':
                    params['latOffset'] = value
                elif key == 'LONG_OFF':
                    params['longOffset'] = value
                elif key == 'HEIGHT_OFF':
                    params['heightOffset'] = value
                elif key == 'LINE_SCALE':
                    params['lineScale'] = value
                elif key == 'SAMP_SCALE':
                    params['sampScale'] = value
                elif key == 'LAT_SCALE':
                    params['latScale'] = value
                elif key == 'LONG_SCALE':
                    params['longScale'] = value
                elif key == 'HEIGHT_SCALE':
                    params['heightScale'] = value
                elif key.startswith('LINE_NUM_COEFF_'):
                    if 'lineNumCoef' not in params:
                        params['lineNumCoef'] = [None] * 20
                    index = int(key.split('_')[-1]) - 1
                    params['lineNumCoef'][index] = value
                elif key.startswith('LINE_DEN_COEFF_'):
                    if 'lineDenCoef' not in params:
                        params['lineDenCoef'] = [None] * 20
                    index = int(key.split('_')[-1]) - 1
                    params['lineDenCoef'][index] = value
                elif key.startswith('SAMP_NUM_COEFF_'):
                    if 'sampNumCoef' not in params:
                        params['sampNumCoef'] = [None] * 20
                    index = int(key.split('_')[-1]) - 1
                    params['sampNumCoef'][index] = value
                elif key.startswith('SAMP_DEN_COEFF_'):
                    if 'sampDenCoef' not in params:
                        params['sampDenCoef'] = [None] * 20
                    index = int(key.split('_')[-1]) - 1
                    params['sampDenCoef'][index] = value
        
        return params
    except Exception as e:
        logger.error(f"解析RPC文件失败: {e}")
        raise


def convert_rpb_to_rpc(input_file, output_file):
    """
    将RPB文件转换为RPC文件
    
    Args:
        input_file (str): 输入RPB文件路径
        output_file (str): 输出RPC文件路径
        
    Returns:
        bool: 转换是否成功
    """
    try:
        # 解析RPB文件
        params = parse_rpb_file(input_file)
        
        # 生成RPC文件内容
        rpc_content = f"LINE_OFF :{params['lineOffset']}  pixels\n"
        rpc_content += f"SAMP_OFF : {params['sampOffset']}  pixels\n"
        rpc_content += f"LAT_OFF : {params['latOffset']}   degrees\n"
        rpc_content += f"LONG_OFF:  {params['longOffset']}   degrees\n"
        rpc_content += f"HEIGHT_OFF: {params['heightOffset']}   meters\n"
        rpc_content += f"LINE_SCALE: {params['lineScale']}  pixels\n"
        rpc_content += f"SAMP_SCALE:  {params['sampScale']}  pixels\n"
        rpc_content += f"LAT_SCALE: {params['latScale']}   degrees\n"
        rpc_content += f"LONG_SCALE: {params['longScale']}   degrees\n"
        rpc_content += f"HEIGHT_SCALE :{params['heightScale']}   meters\n"
        
        # 添加系数
        for i, coef in enumerate(params['lineNumCoef'], 1):
            rpc_content += f"LINE_NUM_COEFF_{i}:{coef}\n"
        
        for i, coef in enumerate(params['lineDenCoef'], 1):
            rpc_content += f"LINE_DEN_COEFF_{i}:{coef}\n"
        
        for i, coef in enumerate(params['sampNumCoef'], 1):
            rpc_content += f"SAMP_NUM_COEFF_{i}:{coef}\n"
        
        for i, coef in enumerate(params['sampDenCoef'], 1):
            rpc_content += f"SAMP_DEN_COEFF_{i}:{coef}\n"
        
        # 写入RPC文件
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(rpc_content)
            
        logger.info(f"成功将RPB文件转换为RPC: {output_file}")
        return True
    except Exception as e:
        logger.error(f"RPB转RPC转换失败: {e}")
        return False


def convert_rpc_to_rpb(input_file, output_file):
    """
    将RPC文件转换为RPB文件
    
    Args:
        input_file (str): 输入RPC文件路径
        output_file (str): 输出RPB文件路径
        
    Returns:
        bool: 转换是否成功
    """
    try:
        # 解析RPC文件
        params = parse_rpc_file(input_file)
        
        # 生成RPB文件内容
        rpb_content = "satId = \"XXX\";\nbandId = \"XXX\";\nSpecId = \"XXX\";\n"
        rpb_content += "BEGIN_GROUP = IMAGE\n"
        rpb_content += "\terrBias =   1.0;\n"
        rpb_content += "\terrRand =    0.0;\n"
        rpb_content += f"\tlineOffset = \t{params['lineOffset']}\n"
        rpb_content += f"\tsampOffset = \t{params['sampOffset']}\n"
        rpb_content += f"\tlatOffset = \t{params['latOffset']}\n"
        rpb_content += f"\tlongOffset = \t{params['longOffset']}\n"
        rpb_content += f"\theightOffset = \t{params['heightOffset']}\n"
        rpb_content += f"\tlineScale = \t{params['lineScale']}\n"
        rpb_content += f"\tsampScale = \t{params['sampScale']}\n"
        rpb_content += f"\tlatScale = \t{params['latScale']}\n"
        rpb_content += f"\tlongScale = \t{params['longScale']}\n"
        rpb_content += f"\theightScale = \t{params['heightScale']}\n"
        
        # 添加系数
        rpb_content += "\tlineNumCoef = (\n"
        rpb_content += "\t\t" + ",\n\t\t".join(params['lineNumCoef']) + ");\n"
        
        rpb_content += "\tlineDenCoef = (\n"
        rpb_content += "\t\t" + ",\n\t\t".join(params['lineDenCoef']) + ");\n"
        
        rpb_content += "\tsampNumCoef = (\n"
        rpb_content += "\t\t" + ",\n\t\t".join(params['sampNumCoef']) + ");\n"
        
        rpb_content += "\tsampDenCoef = (\n"
        rpb_content += "\t\t" + ",\n\t\t".join(params['sampDenCoef']) + ");\n"
        
        rpb_content += "END_GROUP = IMAGE\n"
        rpb_content += "END;"
        
        # 写入RPB文件
        with open(output_file, 'w', encoding='utf-8') as f_out:
            f_out.write(rpb_content)
            
        logger.info(f"成功将RPC文件转换为RPB: {output_file}")
        return True
    except Exception as e:
        logger.error(f"RPC转RPB转换失败: {e}")
        return False


def convert_file(input_file, output_dir):
    """
    根据文件扩展名自动执行文件格式转换
    
    Args:
        input_file (str): 输入文件路径
        output_dir (str): 输出目录路径
        
    Returns:
        bool: 转换是否成功
    """
    # 获取文件名和扩展名
    file_path = Path(input_file)
    file_name = file_path.stem
    file_ext = file_path.suffix.lower()
    
    # 根据扩展名确定转换方向和输出文件名
    if file_ext == ".rpb":
        output_file = os.path.join(output_dir, f"{file_name}.rpc")
        return convert_rpb_to_rpc(input_file, output_file)
    elif file_ext == ".rpc":
        output_file = os.path.join(output_dir, f"{file_name}.rpb")
        return convert_rpc_to_rpb(input_file, output_file)
    else:
        logger.error(f"不支持的文件格式: {file_ext}")
        return False


def main():
    """
    主函数，处理命令行参数并执行转换
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description="RPB/RPC文件格式转换工具")
    parser.add_argument("input_file", help="输入文件路径（.rpb或.rpc格式）")
    parser.add_argument("output_dir", help="输出目录路径")
    parser.add_argument("-v", "--verbose", action="store_true", help="显示详细日志信息")
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 设置日志级别
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # 验证输入参数
    if not validate_input(args.input_file, args.output_dir):
        sys.exit(1)
    
    # 执行文件转换
    if convert_file(args.input_file, args.output_dir):
        logger.info("文件转换成功完成")
        sys.exit(0)
    else:
        logger.error("文件转换失败")
        sys.exit(1)


if __name__ == "__main__":
    main()