import os
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pickle
from pathlib import Path
from typing import Optional
import json

# Gmail API 權限範圍
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

class GmailService:
    def __init__(self):
        self.creds = None
        self.service = None
        self.token_path = Path('gmail_token.pickle')
        
    def _get_client_config(self):
        """從環境變數取得 OAuth 客戶端配置"""
        client_id = os.getenv('GOOGLE_CLIENT_ID')
        client_secret = os.getenv('GOOGLE_CLIENT_SECRET')
        redirect_uri = os.getenv('OAUTH_REDIRECT_URI', 'http://localhost:8000/auth/gmail/callback')
        
        if not client_id or not client_secret:
            raise ValueError(
                "請設定 GOOGLE_CLIENT_ID 和 GOOGLE_CLIENT_SECRET 環境變數"
            )
        
        return {
            "web": {
                "client_id": client_id,
                "client_secret": client_secret,
                "redirect_uris": [redirect_uri],
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token"
            }
        }
    
    def authenticate(self):
        """驗證 Gmail API"""
        # 載入已儲存的憑證
        if self.token_path.exists():
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # 如果沒有有效憑證，進行登入
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                try:
                    self.creds.refresh(Request())
                except Exception as e:
                    print(f"Token 更新失敗: {e}")
                    self.creds = None
            
            if not self.creds:
                # 使用環境變數建立 OAuth 流程
                client_config = self._get_client_config()
                flow = Flow.from_client_config(
                    client_config,
                    scopes=SCOPES,
                    redirect_uri=client_config['web']['redirect_uris'][0]
                )
                
                # 取得授權 URL
                auth_url, _ = flow.authorization_url(
                    access_type='offline',
                    include_granted_scopes='true',
                    prompt='consent'
                )
                
                raise RuntimeError(
                    f"需要 Gmail API 授權。請訪問以下 URL 並授權：\n{auth_url}\n"
                    f"授權後，請使用授權碼呼叫 save_credentials(auth_code) 方法"
                )
            
            # 儲存憑證供下次使用
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        self.service = build('gmail', 'v1', credentials=self.creds)
        return self.service
    
    def save_credentials(self, auth_code: str):
        """使用授權碼儲存憑證"""
        client_config = self._get_client_config()
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=client_config['web']['redirect_uris'][0]
        )
        
        flow.fetch_token(code=auth_code)
        self.creds = flow.credentials
        
        # 儲存憑證
        with open(self.token_path, 'wb') as token:
            pickle.dump(self.creds, token)
        
        return True
    
    def is_authenticated(self) -> bool:
        """檢查是否已認證"""
        if self.token_path.exists():
            try:
                with open(self.token_path, 'rb') as token:
                    creds = pickle.load(token)
                    return creds and creds.valid
            except:
                return False
        return False
    
    def get_auth_url(self) -> str:
        """取得授權 URL"""
        client_config = self._get_client_config()
        flow = Flow.from_client_config(
            client_config,
            scopes=SCOPES,
            redirect_uri=client_config['web']['redirect_uris'][0]
        )
        
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        return auth_url
    
    def create_message(self, to: str, subject: str, message_html: str, 
                      from_email: Optional[str] = None) -> dict:
        """建立郵件訊息"""
        message = MIMEMultipart('alternative')
        message['to'] = to
        message['subject'] = subject
        if from_email:
            message['from'] = from_email
        
        # 加入 HTML 內容
        html_part = MIMEText(message_html, 'html', 'utf-8')
        message.attach(html_part)
        
        # 編碼為 base64
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        return {'raw': raw_message}
    
    def send_email(self, to: str, subject: str, message_html: str) -> dict:
        """發送郵件"""
        try:
            if not self.service:
                self.authenticate()
            
            message = self.create_message(to, subject, message_html)
            sent_message = self.service.users().messages().send(
                userId='me', body=message
            ).execute()
            
            return {
                'success': True,
                'message_id': sent_message['id'],
                'to': to
            }
        except HttpError as error:
            return {
                'success': False,
                'error': str(error),
                'to': to
            }
        except RuntimeError as error:
            # 需要授權
            return {
                'success': False,
                'error': str(error),
                'to': to,
                'needs_auth': True
            }
        except Exception as error:
            return {
                'success': False,
                'error': str(error),
                'to': to
            }
    
    def render_template(self, template_content: str, variables: dict) -> str:
        """渲染郵件模板"""
        content = template_content
        for key, value in variables.items():
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))
        return content

# 單例模式
gmail_service = GmailService()
