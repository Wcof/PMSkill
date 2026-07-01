// TODO: 添加年付选项支持
export async function login(phone: string, code: string) {
  // FIXME: 验证码错误 3 次未锁定（安全风险）
  return verifyCode(phone, code);
}
