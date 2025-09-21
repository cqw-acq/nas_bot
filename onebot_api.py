#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OneBot 11 API调用模块
提供完整的NapCat API调用功能
"""

import json
import time
import logging
from typing import Dict, Any, List, Optional, Union
import requests


logger = logging.getLogger(__name__)


class OneBotAPI:
    """OneBot API调用类"""
    
    def __init__(self, host: str = 'localhost', port: int = 3000, token: str = ''):
        self.base_url = f"http://{host}:{port}"
        self.token = token
        self.headers = {'Content-Type': 'application/json'}
        
        if self.token:
            self.headers['Authorization'] = f"Bearer {self.token}"
    
    def _call_api(self, endpoint: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """调用API的基础方法"""
        url = f"{self.base_url}/{endpoint}"
        
        try:
            if data is None:
                response = requests.get(url, headers=self.headers, timeout=10)
            else:
                response = requests.post(url, json=data, headers=self.headers, timeout=10)
            
            response.raise_for_status()
            
            try:
                result = response.json()
            except json.JSONDecodeError as e:
                error_msg = f"API响应JSON解析失败: {e}, 响应内容: {response.text}"
                logger.error(error_msg)
                return {
                    'status': 'failed', 
                    'retcode': -2, 
                    'msg': 'API响应JSON解析失败',
                    'details': str(e),
                    'response_text': response.text
                }
            
            if result.get('status') == 'failed':
                logger.error(f"API调用失败: {result.get('msg', '未知错误')}")
                return result
            
            logger.debug(f"API调用成功: {endpoint}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"API请求异常: {e}")
            return {'status': 'failed', 'retcode': -1, 'msg': str(e)}
        except Exception as e:
            logger.error(f"API调用异常: {e}")
            return {'status': 'failed', 'retcode': -1, 'msg': str(e)}
    
    # 消息发送相关API
    def send_private_msg(self, user_id: Union[int, str], message: str, auto_escape: bool = False) -> Dict[str, Any]:
        """发送私聊消息"""
        data = {
            'user_id': int(user_id),
            'message': message,
            'auto_escape': auto_escape
        }
        return self._call_api('send_private_msg', data)
    
    def send_group_msg(self, group_id: Union[int, str], message: str, auto_escape: bool = False) -> Dict[str, Any]:
        """发送群消息"""
        data = {
            'group_id': int(group_id),
            'message': message,
            'auto_escape': auto_escape
        }
        return self._call_api('send_group_msg', data)
    
    def send_msg(self, message_type: str, user_id: Union[int, str] = None, 
                 group_id: Union[int, str] = None, message: str = '', 
                 auto_escape: bool = False) -> Dict[str, Any]:
        """发送消息（统一接口）"""
        data = {
            'message_type': message_type,
            'message': message,
            'auto_escape': auto_escape
        }
        
        if message_type == 'private' and user_id:
            data['user_id'] = int(user_id)
        elif message_type == 'group' and group_id:
            data['group_id'] = int(group_id)
        else:
            raise ValueError("消息类型和目标ID不匹配")
        
        return self._call_api('send_msg', data)
    
    def delete_msg(self, message_id: Union[int, str]) -> Dict[str, Any]:
        """撤回消息"""
        data = {'message_id': int(message_id)}
        return self._call_api('delete_msg', data)
    
    # 消息获取相关API
    def get_msg(self, message_id: Union[int, str]) -> Dict[str, Any]:
        """获取消息"""
        data = {'message_id': int(message_id)}
        return self._call_api('get_msg', data)
    
    def get_forward_msg(self, id: str) -> Dict[str, Any]:
        """获取合并转发消息"""
        data = {'id': id}
        return self._call_api('get_forward_msg', data)
    
    # 好友相关API
    def get_login_info(self) -> Dict[str, Any]:
        """获取登录号信息"""
        return self._call_api('get_login_info')
    
    def get_stranger_info(self, user_id: Union[int, str], no_cache: bool = False) -> Dict[str, Any]:
        """获取陌生人信息"""
        data = {
            'user_id': int(user_id),
            'no_cache': no_cache
        }
        return self._call_api('get_stranger_info', data)
    
    def get_friend_list(self) -> Dict[str, Any]:
        """获取好友列表"""
        return self._call_api('get_friend_list')
    
    # 群组相关API
    def get_group_info(self, group_id: Union[int, str], no_cache: bool = False) -> Dict[str, Any]:
        """获取群信息"""
        data = {
            'group_id': int(group_id),
            'no_cache': no_cache
        }
        return self._call_api('get_group_info', data)
    
    def get_group_list(self) -> Dict[str, Any]:
        """获取群列表"""
        return self._call_api('get_group_list')
    
    def get_group_member_info(self, group_id: Union[int, str], user_id: Union[int, str], 
                             no_cache: bool = False) -> Dict[str, Any]:
        """获取群成员信息"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'no_cache': no_cache
        }
        return self._call_api('get_group_member_info', data)
    
    def get_group_member_list(self, group_id: Union[int, str]) -> Dict[str, Any]:
        """获取群成员列表"""
        data = {'group_id': int(group_id)}
        return self._call_api('get_group_member_list', data)
    
    def get_group_honor_info(self, group_id: Union[int, str], type: str = 'all') -> Dict[str, Any]:
        """获取群荣誉信息"""
        data = {
            'group_id': int(group_id),
            'type': type
        }
        return self._call_api('get_group_honor_info', data)
    
    # 群管理相关API
    def set_group_kick(self, group_id: Union[int, str], user_id: Union[int, str], 
                      reject_add_request: bool = False) -> Dict[str, Any]:
        """群组踢人"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'reject_add_request': reject_add_request
        }
        return self._call_api('set_group_kick', data)
    
    def set_group_ban(self, group_id: Union[int, str], user_id: Union[int, str], 
                     duration: int = 30 * 60) -> Dict[str, Any]:
        """群组单人禁言"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'duration': duration
        }
        return self._call_api('set_group_ban', data)
    
    def set_group_anonymous_ban(self, group_id: Union[int, str], anonymous: Dict[str, Any], 
                               duration: int = 30 * 60) -> Dict[str, Any]:
        """群组匿名用户禁言"""
        data = {
            'group_id': int(group_id),
            'anonymous': anonymous,
            'duration': duration
        }
        return self._call_api('set_group_anonymous_ban', data)
    
    def set_group_whole_ban(self, group_id: Union[int, str], enable: bool = True) -> Dict[str, Any]:
        """群组全员禁言"""
        data = {
            'group_id': int(group_id),
            'enable': enable
        }
        return self._call_api('set_group_whole_ban', data)
    
    def set_group_admin(self, group_id: Union[int, str], user_id: Union[int, str], 
                       enable: bool = True) -> Dict[str, Any]:
        """群组设置管理员"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'enable': enable
        }
        return self._call_api('set_group_admin', data)
    
    def set_group_anonymous(self, group_id: Union[int, str], enable: bool = True) -> Dict[str, Any]:
        """群组匿名"""
        data = {
            'group_id': int(group_id),
            'enable': enable
        }
        return self._call_api('set_group_anonymous', data)
    
    def set_group_card(self, group_id: Union[int, str], user_id: Union[int, str], 
                      card: str = '') -> Dict[str, Any]:
        """设置群名片（群备注）"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'card': card
        }
        return self._call_api('set_group_card', data)
    
    def set_group_name(self, group_id: Union[int, str], group_name: str) -> Dict[str, Any]:
        """设置群名"""
        data = {
            'group_id': int(group_id),
            'group_name': group_name
        }
        return self._call_api('set_group_name', data)
    
    def set_group_leave(self, group_id: Union[int, str], is_dismiss: bool = False) -> Dict[str, Any]:
        """退出群组"""
        data = {
            'group_id': int(group_id),
            'is_dismiss': is_dismiss
        }
        return self._call_api('set_group_leave', data)
    
    def set_group_special_title(self, group_id: Union[int, str], user_id: Union[int, str], 
                               special_title: str = '', duration: int = -1) -> Dict[str, Any]:
        """设置群组专属头衔"""
        data = {
            'group_id': int(group_id),
            'user_id': int(user_id),
            'special_title': special_title,
            'duration': duration
        }
        return self._call_api('set_group_special_title', data)
    
    # 请求处理相关API
    def set_friend_add_request(self, flag: str, approve: bool = True, 
                              remark: str = '') -> Dict[str, Any]:
        """处理加好友请求"""
        data = {
            'flag': flag,
            'approve': approve,
            'remark': remark
        }
        return self._call_api('set_friend_add_request', data)
    
    def set_group_add_request(self, flag: str, sub_type: str, approve: bool = True, 
                             reason: str = '') -> Dict[str, Any]:
        """处理加群请求／邀请"""
        data = {
            'flag': flag,
            'sub_type': sub_type,
            'approve': approve,
            'reason': reason
        }
        return self._call_api('set_group_add_request', data)
    
    # 其他API
    def get_cookies(self, domain: str = '') -> Dict[str, Any]:
        """获取Cookies"""
        data = {'domain': domain}
        return self._call_api('get_cookies', data)
    
    def get_csrf_token(self) -> Dict[str, Any]:
        """获取CSRF Token"""
        return self._call_api('get_csrf_token')
    
    def get_credentials(self, domain: str = '') -> Dict[str, Any]:
        """获取QQ相关接口凭证"""
        data = {'domain': domain}
        return self._call_api('get_credentials', data)
    
    def get_record(self, file: str, out_format: str = 'mp3') -> Dict[str, Any]:
        """获取语音"""
        data = {
            'file': file,
            'out_format': out_format
        }
        return self._call_api('get_record', data)
    
    def get_image(self, file: str) -> Dict[str, Any]:
        """获取图片"""
        data = {'file': file}
        return self._call_api('get_image', data)
    
    def can_send_image(self) -> Dict[str, Any]:
        """检查是否可以发送图片"""
        return self._call_api('can_send_image')
    
    def can_send_record(self) -> Dict[str, Any]:
        """检查是否可以发送语音"""
        return self._call_api('can_send_record')
    
    def get_status(self) -> Dict[str, Any]:
        """获取运行状态"""
        return self._call_api('get_status')
    
    def get_version_info(self) -> Dict[str, Any]:
        """获取版本信息"""
        return self._call_api('get_version_info')
    
    def set_restart(self, delay: int = 0) -> Dict[str, Any]:
        """重启OneBot实现"""
        data = {'delay': delay}
        return self._call_api('set_restart', data)
    
    def clean_cache(self) -> Dict[str, Any]:
        """清理缓存"""
        return self._call_api('clean_cache')


class MessageBuilder:
    """消息构建器"""
    
    @staticmethod
    def text(text: str) -> str:
        """构建文本消息"""
        return text
    
    @staticmethod
    def at(user_id: Union[int, str], name: str = '') -> str:
        """构建@消息"""
        if name:
            return f"[CQ:at,qq={user_id},name={name}]"
        return f"[CQ:at,qq={user_id}]"
    
    @staticmethod
    def at_all() -> str:
        """构建@全体成员消息"""
        return "[CQ:at,qq=all]"
    
    @staticmethod
    def face(id: int) -> str:
        """构建表情消息"""
        return f"[CQ:face,id={id}]"
    
    @staticmethod
    def image(file: str, type: str = 'image', cache: int = 1) -> str:
        """构建图片消息"""
        return f"[CQ:image,file={file},type={type},cache={cache}]"
    
    @staticmethod
    def record(file: str, magic: int = 0) -> str:
        """构建语音消息"""
        return f"[CQ:record,file={file},magic={magic}]"
    
    @staticmethod
    def video(file: str, cover: str = '') -> str:
        """构建视频消息"""
        if cover:
            return f"[CQ:video,file={file},cover={cover}]"
        return f"[CQ:video,file={file}]"
    
    @staticmethod
    def music(type: str, id: Union[int, str]) -> str:
        """构建音乐分享消息"""
        return f"[CQ:music,type={type},id={id}]"
    
    @staticmethod
    def custom_music(url: str, audio: str, title: str, content: str = '', image: str = '') -> str:
        """构建自定义音乐分享消息"""
        return f"[CQ:music,type=custom,url={url},audio={audio},title={title},content={content},image={image}]"
    
    @staticmethod
    def share(url: str, title: str, content: str = '', image: str = '') -> str:
        """构建链接分享消息"""
        return f"[CQ:share,url={url},title={title},content={content},image={image}]"
    
    @staticmethod
    def reply(id: Union[int, str]) -> str:
        """构建回复消息"""
        return f"[CQ:reply,id={id}]"
    
    @staticmethod
    def forward(id: str) -> str:
        """构建合并转发消息"""
        return f"[CQ:forward,id={id}]"
    
    @staticmethod
    def combine(*messages: str) -> str:
        """组合多个消息"""
        return ''.join(messages)