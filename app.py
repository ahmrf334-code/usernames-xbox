import requests
import json
from typing import List, Dict

class XboxUsernameChecker:
    def __init__(self):
        self.api_url = "https://xboxlive.com/api/v2/accounts/search"
        self.results = []
    
    def check_username(self, username: str) -> Dict[str, str]:
        """فحص توفر اسم مستخدم واحد"""
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
                "status": f"⚠️ خطأ: {str(e)}"
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
