#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
JSON处理工具模块
提供JSON数据清理和解析的实用函数
"""

import json
import re
import logging
from typing import Dict, Any, Tuple, Optional


logger = logging.getLogger(__name__)


def clean_json_string(data: str) -> str:
    """
    清理JSON字符串中的控制字符
    
    Args:
        data: 原始JSON字符串
        
    Returns:
        清理后的JSON字符串
    """
    # 移除常见的控制字符（保留换行符\n、回车符\r和制表符\t）
    cleaned = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', data)
    
    # 记录是否进行了清理
    if cleaned != data:
        removed_chars = len(data) - len(cleaned)
        logger.warning(f"移除了 {removed_chars} 个控制字符")
        
        # 分析被移除的字符
        control_chars = []
        for i, char in enumerate(data):
            if ord(char) in range(0, 9) or ord(char) in range(11, 13) or ord(char) in range(14, 32) or ord(char) == 127:
                control_chars.append(f"位置{i}: 0x{ord(char):02x}")
        
        if control_chars:
            logger.debug(f"移除的控制字符: {', '.join(control_chars[:10])}")  # 只显示前10个
    
    return cleaned


def safe_json_decode(data: bytes) -> Tuple[str, Optional[str]]:
    """
    安全解码字节数据为字符串
    
    Args:
        data: 字节数据
        
    Returns:
        (解码后的字符串, 错误信息)
    """
    try:
        return data.decode('utf-8'), None
    except UnicodeDecodeError as e:
        error_msg = f"UTF-8解码失败: {e}"
        logger.warning(error_msg)
        
        # 尝试其他编码
        encodings = ['gbk', 'gb2312', 'latin1', 'cp1252']
        for encoding in encodings:
            try:
                decoded = data.decode(encoding)
                logger.info(f"使用 {encoding} 编码成功解码")
                return decoded, None
            except UnicodeDecodeError:
                continue
        
        # 所有编码都失败，使用replace模式
        decoded = data.decode('utf-8', errors='replace')
        return decoded, error_msg


def parse_json_with_details(data: str) -> Tuple[Optional[Dict[Any, Any]], Optional[Dict[str, Any]]]:
    """
    解析JSON并提供详细的错误信息
    
    Args:
        data: JSON字符串
        
    Returns:
        (解析结果, 错误详情字典)
    """
    try:
        # 首先清理数据
        cleaned_data = clean_json_string(data)
        
        # 尝试解析
        result = json.loads(cleaned_data)
        return result, None
        
    except json.JSONDecodeError as e:
        error_position = getattr(e, 'pos', 0)
        
        # 分析错误位置周围的字符
        start_pos = max(0, error_position - 15)
        end_pos = min(len(data), error_position + 15)
        context = data[start_pos:end_pos]
        
        # 获取错误字符的详细信息
        error_char = data[error_position] if error_position < len(data) else ''
        error_char_hex = f'0x{ord(error_char):02x}' if error_char else 'EOF'
        error_char_repr = repr(error_char) if error_char else 'EOF'
        
        # 显示十六进制字符以便分析控制字符
        hex_context = ' '.join(f'{ord(c):02x}' for c in context)
        
        # 尝试常见的修复方法
        suggestions = []
        
        # 检查是否有未闭合的引号
        if data.count('"') % 2 != 0:
            suggestions.append("检查是否有未闭合的引号")
        
        # 检查是否有多余的逗号
        if ',}' in data or ',]' in data:
            suggestions.append("检查是否有多余的逗号")
        
        # 检查是否有未转义的字符
        if '\\' not in data and ('"' in data[1:-1] if len(data) > 2 else False):
            suggestions.append("检查是否有未转义的引号")
        
        error_details = {
            'error_type': 'JSON解析失败',
            'error_message': str(e),
            'error_position': error_position,
            'error_char': error_char_repr,
            'error_char_hex': error_char_hex,
            'context': context,
            'context_repr': repr(context),
            'hex_context': hex_context,
            'data_length': len(data),
            'suggestions': suggestions,
            'line_column': f"line {getattr(e, 'lineno', '?')} column {getattr(e, 'colno', '?')}"
        }
        
        return None, error_details


def log_json_error(error_details: Dict[str, Any], logger_instance: logging.Logger = None):
    """
    记录详细的JSON解析错误信息
    
    Args:
        error_details: 错误详情字典
        logger_instance: 日志记录器实例
    """
    if logger_instance is None:
        logger_instance = logger
    
    logger_instance.error(f"JSON解析失败: {error_details['error_message']}")
    logger_instance.error(f"错误位置: {error_details['error_position']} ({error_details['line_column']})")
    logger_instance.error(f"错误字符: {error_details['error_char']} ({error_details['error_char_hex']})")
    logger_instance.error(f"上下文: {error_details['context_repr']}")
    logger_instance.error(f"十六进制: {error_details['hex_context']}")
    logger_instance.error(f"数据长度: {error_details['data_length']}")
    
    if error_details['suggestions']:
        logger_instance.info(f"建议修复方法: {'; '.join(error_details['suggestions'])}")


def create_error_response(error_details: Dict[str, Any], include_raw_data: bool = True, 
                         raw_data: str = None) -> Dict[str, Any]:
    """
    创建标准化的错误响应
    
    Args:
        error_details: 错误详情字典
        include_raw_data: 是否包含原始数据
        raw_data: 原始数据字符串
        
    Returns:
        错误响应字典
    """
    response = {
        'status': 'failed',
        'error': error_details['error_type'],
        'details': error_details['error_message'],
        'error_position': error_details['error_position'],
        'error_char': error_details['error_char'],
        'context': error_details['context'],
        'hex_context': error_details['hex_context'],
        'data_length': error_details['data_length'],
        'suggestions': error_details['suggestions']
    }
    
    if include_raw_data and raw_data is not None:
        response['raw_data'] = raw_data
    
    return response


# 便捷函数
def safe_parse_json(data: bytes) -> Tuple[Optional[Dict[Any, Any]], Optional[Dict[str, Any]]]:
    """
    安全解析JSON字节数据的便捷函数
    
    Args:
        data: JSON字节数据
        
    Returns:
        (解析结果, 错误响应字典)
    """
    # 解码数据
    decoded_data, decode_error = safe_json_decode(data)
    
    if decode_error:
        logger.error(f"数据解码失败: {decode_error}")
    
    # 解析JSON
    result, error_details = parse_json_with_details(decoded_data)
    
    if error_details:
        log_json_error(error_details)
        error_response = create_error_response(error_details, raw_data=decoded_data)
        return None, error_response
    
    return result, None