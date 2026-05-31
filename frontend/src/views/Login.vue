<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <el-icon size="48" color="#667eea"><School /></el-icon>
        <h2>欢迎回来</h2>
        <p>登录安徽理工大学贴吧</p>
      </div>
      
      <el-form :model="form" :rules="rules" ref="formRef" class="auth-form">
        <el-form-item prop="username">
          <el-input
            v-model="form.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="submit-btn"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <div class="auth-footer">
        <p>还没有账号？<router-link to="/register">立即注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import axios from 'axios'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const formRef = ref(null)
    const loading = ref(false)
    
    const form = reactive({
      username: '',
      password: ''
    })
    
    const rules = {
      username: [
        { required: true, message: '请输入用户名', trigger: 'blur' },
        { min: 3, max: 20, message: '长度在 3 到 20 个字符', trigger: 'blur' }
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
        { min: 6, message: '密码至少6位', trigger: 'blur' }
      ]
    }
    
    const handleLogin = async () => {
      const valid = await formRef.value.validate().catch(() => false)
      if (!valid) return
      
      loading.value = true
      try {
        const response = await axios.post('/api/login', form)
        localStorage.setItem('token', response.data.token)
        localStorage.setItem('user', JSON.stringify(response.data.user))
        ElMessage.success('登录成功')
        router.push('/')
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '登录失败')
      } finally {
        loading.value = false
      }
    }
    
    return {
      form,
      formRef,
      rules,
      loading,
      handleLogin,
      User,
      Lock
    }
  }
}
</script>

<style scoped>
.auth-page {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 200px);
  padding: 20px;
}

.auth-card {
  background: white;
  border-radius: 16px;
  padding: 40px;
  width: 100%;
  max-width: 420px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.auth-header {
  text-align: center;
  margin-bottom: 32px;
}

.auth-header h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin: 16px 0 8px;
}

.auth-header p {
  color: #999;
  font-size: 14px;
}

.auth-form :deep(.el-input__wrapper) {
  border-radius: 8px;
}

.submit-btn {
  width: 100%;
  border-radius: 8px;
  font-size: 16px;
}

.auth-footer {
  text-align: center;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px solid #f0f0f0;
}

.auth-footer a {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
}

.auth-footer a:hover {
  text-decoration: underline;
}
</style>