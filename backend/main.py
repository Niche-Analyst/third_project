import os
import mariadb
from jose import jwt
from fastapi import FastAPI, Depends, HTTPException, Header
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수에서 민감한 정보를 가져옵니다.
SUPABASE_JWT_SECRET = os.getenv("SUPABASE_JWT_SECRET")
MARIADB_HOST = os.getenv("MARIADB_HOST")
MARIADB_USER = os.getenv("MARIADB_USER")
MARIADB_PASSWORD = os.getenv("MARIADB_PASSWORD")
MARIADB_DATABASE = os.getenv("MARIADB_DATABASE")

# 환경 변수가 제대로 로드되었는지 확인합니다.
if not all([SUPABASE_JWT_SECRET, MARIADB_HOST, MARIADB_USER, MARIADB_PASSWORD, MARIADB_DATABASE]):
    raise ValueError("One or more environment variables are not set. Please check your .env file.")

# API 요청으로 받을 데이터 모델
class UserActivity(BaseModel):
    activity_type: str
    data: str

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db_connection():
    """MariaDB 데이터베이스 연결을 생성하고 반환합니다."""
    try:
        conn = mariadb.connect(
            host=MARIADB_HOST,
            user=MARIADB_USER,
            password=MARIADB_PASSWORD,
            database=MARIADB_DATABASE
        )
        return conn
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB: {e}")
        raise HTTPException(status_code=500, detail="Database connection failed")

def get_current_user_uuid(authorization: str = Header(...)):
    """JWT 토큰을 검증하고 사용자 UUID를 추출합니다."""
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SUPABASE_JWT_SECRET, algorithms=["HS256"])
        user_uuid = payload.get("sub")
        
        if not user_uuid:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        
        return user_uuid
    except (jwt.PyJWTError, IndexError) as e:
        print(f"Token validation error: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/api/save-activity")
def save_user_activity(
    activity: UserActivity,
    user_uuid: str = Depends(get_current_user_uuid)
):
    """사용자 활동 데이터를 MariaDB에 저장하는 API 엔드포인트."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute(
            "INSERT INTO user_activities (user_uuid, activity_type, data) VALUES (?, ?, ?)",
            (user_uuid, activity.activity_type, activity.data)
        )
        conn.commit()
    except mariadb.Error as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=f"Database insertion failed: {e}")
    finally:
        cursor.close()
        conn.close()
    
    return {"message": "Activity saved successfully."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)