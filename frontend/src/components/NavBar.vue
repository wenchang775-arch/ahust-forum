<template>
  <nav class="navbar">
    <div class="nav-container">
      <router-link to="/" class="logo">
        <el-icon size="28"><School /></el-icon>
        <span>安徽理工大学贴吧</span>
      </router-link>
      
      <div class="nav-search">
        <el-input
          v-model="searchKeyword"
          placeholder="搜索帖子..."
          @keyup.enter="handleSearch"
          clearable
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
      </div>
      
      <div class="nav-actions">
        <template v-if="isLoggedIn">
          <el-button type="primary" @click="$router.push('/create')">
            <el-icon><Plus /></el-icon>
            发帖
          </el-button>
          <el-dropdown @command="handleCommand">
            <span class="user-info">
              <el-avatar :size="36" :src="user?.avatar || ''">
                <el-icon><User /></el-icon>
              </el-avatar>
              <span class="username">{{ user?.username }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>
                  个人中心
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button @click="$router.push('/login')">登录</el-button>
          <el-button type="primary" @click="$router.push('/register')">注册</el-button>
        </template>
      </div>
    </div>
  </nav>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import axios from 'axios'

export default {
  name: 'NavBar',
  setup() {
    const router = useRouter()
    const searchKeyword = ref('')
    const user = ref(null)
    
    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('token')
    })
    
    const fetchUserInfo = async () => {
      const token = localStorage.getItem('token')
      if (!token) return
      
      try {
        const response = await axios.get('/api/user', {
          headers: { Authorization: `Bearer ${token}` }
        })
        user.value = response.data
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }
    
    const handleSearch = () => {
      if (searchKeyword.value.trim()) {
        router.push(`/search?q=${encodeURIComponent(searchKeyword.value.trim())}`)
      }
    }
    
    const handleCommand = (command) => {
      if (command === 'profile') {
        router.push('/profile')
      } else if (command === 'logout') {
        localStorage.removeItem('token')
        user.value = null
        ElMessage.success('已退出登录')
        router.push('/')
      }
    }
    
    onMounted(() => {
      fetchUserInfo()
    })
    
    return {
      searchKeyword,
      isLoggedIn,
      user,
      handleSearch,
      handleCommand
    }
  }
}
</script>

<style scoped>
.navbar {
  background: white;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: #667eea;
  font-size: 20px;
  font-weight: 600;
}

.nav-search {
  flex: 1;
  max-width: 400px;
  margin: 0 40px;
}

.nav-search :deep(.el-input__wrapper) {
  border-radius: 20px;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 16px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 20px;
  transition: background 0.3s;
}

.user-info:hover {
  background: #f5f5f5;
}

.username {
  font-size: 14px;
  color: #333;
  max-width: 100px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>