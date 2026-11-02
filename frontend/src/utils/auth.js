//  存储token、存储用户信息、获取token、用户信息，删除token、用户信息这些作用
const TOKEN_KEY = 'token'
const USER_KEY = 'userInfo'

export function getToken() {
  //获取
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token) {
  //存储
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken() {
  //删除
  localStorage.removeItem(TOKEN_KEY)
}

export function getUserInfo() {
  const str = localStorage.getItem(USER_KEY)
  return str ? JSON.parse(str) : null
}

export function setUserInfo(userInfo) {
  localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
}

export function removeUserInfo() {
  localStorage.removeItem(USER_KEY)
}

// 登出
export function logout() {
  removeToken()
  removeUserInfo()
}
