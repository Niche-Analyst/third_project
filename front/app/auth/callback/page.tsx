"use client";

import { useEffect } from "react";
import { supabase } from "../supabaseClient";
import { useRouter } from "next/navigation";
import CryptoJS from "crypto-js";

// !!! 경고: 이 키는 절대로 코드에 직접 하드코딩하면 안 됩니다. !!!
// !!! Next.js 환경 변수로 관리하세요. (예: process.env.ENCRYPTION_SECRET_KEY) !!!
const ENCRYPTION_SECRET_KEY = "Security_Key"; 

export default function CallbackPage() {
  const router = useRouter();

  useEffect(() => {
    async function handleAuth() {
      // 1. URL의 토큰을 자동으로 가져와 Supabase 세션을 설정합니다.
      const { data: { session }, error } = await supabase.auth.getSession();

      if (error) {
        console.error("OAuth callback error:", error.message);
        return;
      }

      console.log("User session:", session);

      // 2. 세션이 성공적으로 설정되면 데이터 삽입 함수를 호출합니다.
      if (session) {
        await insertOrUpdateUserProfile(session);
        await insertUserTokens(session);
      }

      // 3. 모든 로직이 완료된 후 사용자를 홈 페이지로 리다이렉트합니다.
      router.push("/");
    }

    handleAuth();
  }, [router]);

  return <div>처리 중...</div>;
}

// 사용자의 프로필을 삽입/업데이트하는 함수
// 로그인 후 `profiles` 테이블에 사용자 정보를 저장합니다.
async function insertOrUpdateUserProfile(session: any) {
  const user = session.user;
  const { error } = await supabase
    .from('profiles')
    .upsert({
      id: user.id,
      email: user.email,
      full_name: user.user_metadata.full_name,
    }, { onConflict: 'id' });

  if (error) {
    console.error("프로필 삽입/업데이트 실패:", error);
  }
}

// 사용자의 토큰을 암호화하여 삽입하는 함수
async function insertUserTokens(session: any) {
  const user = session.user;
  const { access_token, refresh_token, expires_at } = session;

  // refresh_token을 암호화
  const encryptedRefreshToken = encryptToken(refresh_token);

  const { error } = await supabase
    .from('user_tokens')
    .upsert({
      user_id: user.id,
      access_token,
      refresh_token: encryptedRefreshToken, // 암호화된 토큰을 저장
      expires_at: new Date(expires_at * 1000), 
    }, { onConflict: 'user_id' });

  if (error) {
    console.error("사용자 토큰 삽입 실패:", error);
  }
}

// 토큰을 암호화하는 함수
function encryptToken(token: string): string {
  return CryptoJS.AES.encrypt(token, ENCRYPTION_SECRET_KEY).toString();
}

// 토큰을 복호화하는 함수 (필요할 때 사용)
function decryptToken(encryptedToken: string): string {
  const bytes = CryptoJS.AES.decrypt(encryptedToken, ENCRYPTION_SECRET_KEY);
  return bytes.toString(CryptoJS.enc.Utf8);
}