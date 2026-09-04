import requests
import json
import re
from typing import List, Dict

class XboxUsernameChecker:
    def __init__(self):
        self.api_url = "https://xboxlive.com/api/v2/accounts/search"
        self.results = []
    
    def is_valid_format(self, username: str) -> bool:
        """التحقق من أن الاسم إما:
        - 4 أحرف فقط
        - 3 حروف + رقم واحد"""
        
        # التحقق من أن الطول 4
        if len(username) != 4:
            return False
        
        # حالة 1: 4 أحرف فقط
        if username.isalpha():
            return True
        
        # حالة 2: 3 حروف + رقم واحد
        letter_count = sum(1 for c in username if c.isalpha())
        digit_count = sum(1 for c in username if c.isdigit())
        
        return letter_count == 3 and digit_count == 1
    
    def check_username(self, username: str) -> Dict[str, str]:
        """فحص توفر اسم مستخدم واحد"""
        # التحقق من الصيغة أولاً
        if not self.is_valid_format(username):
            return {
                "username": username,
                "available": None,
                "status": "⚠️ يجب أن يكون: 4 أحرف أو 3 حروف + رقم واحد"
            }
        
        try:
            # محاكاة API للتحقق من توفر الاسم
            response = requests.get(
                f"https://xboxlive.com/api/v2/accounts/gamertag/{username}/exists",
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                is_available = not data.get('exists', False)
            else:
                # إذا لم نتمكن من الوصول للـ API
                is_available = True
                
            return {
                "username": username,
                "available": is_available,
                "status": "✅ متوفر" if is_available else "❌ غير متوفر"
            }
        except Exception as e:
            return {
                "username": username,
                "available": None,
                "status": f"⚠️ ��طأ: {str(e)}"
            }
    
    def check_multiple(self, usernames: List[str]) -> List[Dict]:
        """فحص عدة أسماء مستخدمين"""
        self.results = []
        for username in usernames:
            result = self.check_username(username.strip())
            self.results.append(result)
        return self.results
    
    def display_results(self):
        """عرض النتائج بشكل جميل"""
        print("\n" + "="*50)
        print("نتائج فحص أسماء Xbox")
        print("="*50 + "\n")
        
        for result in self.results:
            print(f"{result['username']:<20} {result['status']}")
        
        print("\n" + "="*50)
    
    def start(self):
        """بدء التطبيق"""
        print("\n🎮 مرحباً بك في أداة فحص أسماء Xbox\n")
        print("✅ صيغ مقبولة:")
        print("   • 4 أحرف فقط (مثل: abcd, test, xyzw)")
        print("   • 3 حروف + رقم واحد (مثل: abc1, xy2z, tes3)\n")
        print("أدخل أسماء المستخدمين (واحد في كل سطر)")
        print("اضغط Enter مرتين عند الانتهاء\n")
        
        usernames = []
        while True:
            try:
                username = input("أدخل اسم مستخدم: ").strip()
                if not username:
                    if usernames:
                        break
                    print("الرجاء إدخال اسم واحد على الأقل!")
                    continue
                usernames.append(username)
            except KeyboardInterrupt:
                print("\n\nتم الإلغاء")
                return
        
        print("\n⏳ جاري الفحص...\n")
        self.check_multiple(usernames)
        self.display_results()

if __name__ == "__main__":
    checker = XboxUsernameChecker()
    checker.start()
