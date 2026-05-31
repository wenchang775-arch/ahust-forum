import axios from 'axios'

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || '',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器，添加token
apiClient.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

export default apiClient
