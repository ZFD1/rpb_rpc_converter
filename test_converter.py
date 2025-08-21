#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试RPB/RPC文件格式转换工具

该脚本用于测试rpb_rpc_converter.py的功能
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

# 导入转换工具模块
import rpb_rpc_converter as converter


class TestRpbRpcConverter(unittest.TestCase):
    """
    测试RPB/RPC文件格式转换工具的功能
    """
    
    def setUp(self):
        """
        测试前的准备工作
        """
        # 创建临时目录用于测试
        self.test_dir = tempfile.mkdtemp()
        self.output_dir = os.path.join(self.test_dir, "output")
        os.makedirs(self.output_dir, exist_ok=True)
        
        # 创建测试文件
        self.rpb_file = os.path.join(self.test_dir, "test.rpb")
        self.rpc_file = os.path.join(self.test_dir, "test.rpc")
        
        # 写入一些测试数据
        with open(self.rpb_file, "wb") as f:
            f.write(b"This is a test RPB file")
            
        with open(self.rpc_file, "wb") as f:
            f.write(b"This is a test RPC file")
    
    def tearDown(self):
        """
        测试后的清理工作
        """
        # 删除临时目录
        shutil.rmtree(self.test_dir)
    
    def test_validate_input(self):
        """
        测试输入验证功能
        """
        # 测试有效输入
        self.assertTrue(converter.validate_input(self.rpb_file, self.output_dir))
        self.assertTrue(converter.validate_input(self.rpc_file, self.output_dir))
        
        # 测试不存在的文件
        non_existent_file = os.path.join(self.test_dir, "non_existent.rpb")
        self.assertFalse(converter.validate_input(non_existent_file, self.output_dir))
        
        # 测试不支持的文件格式
        invalid_file = os.path.join(self.test_dir, "invalid.txt")
        with open(invalid_file, "w") as f:
            f.write("This is an invalid file")
        self.assertFalse(converter.validate_input(invalid_file, self.output_dir))
    
    def test_rpb_to_rpc_conversion(self):
        """
        测试RPB到RPC的转换
        """
        # 执行转换
        result = converter.convert_file(self.rpb_file, self.output_dir)
        self.assertTrue(result)
        
        # 检查输出文件是否存在
        output_file = os.path.join(self.output_dir, "test.rpc")
        self.assertTrue(os.path.exists(output_file))
    
    def test_rpc_to_rpb_conversion(self):
        """
        测试RPC到RPB的转换
        """
        # 执行转换
        result = converter.convert_file(self.rpc_file, self.output_dir)
        self.assertTrue(result)
        
        # 检查输出文件是否存在
        output_file = os.path.join(self.output_dir, "test.rpb")
        self.assertTrue(os.path.exists(output_file))
    
    def test_convert_file_function(self):
        """
        测试文件转换功能
        """
        # 测试RPB到RPC的转换
        result1 = converter.convert_file(self.rpb_file, self.output_dir)
        self.assertTrue(result1)
        
        # 测试RPC到RPB的转换
        result2 = converter.convert_file(self.rpc_file, self.output_dir)
        self.assertTrue(result2)
        
        # 测试不支持的文件格式
        invalid_file = os.path.join(self.test_dir, "invalid.txt")
        with open(invalid_file, "w") as f:
            f.write("This is an invalid file")
        result3 = converter.convert_file(invalid_file, self.output_dir)
        self.assertFalse(result3)


if __name__ == "__main__":
    unittest.main()