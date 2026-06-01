<template>
  <div class="profile-page">
    <div class="profile-header card">
      <div class="avatar-section">
        <el-avatar :size="80" :src="user?.avatar || ''">
          <el-icon size="40"><User /></el-icon>
        </el-avatar>
        <el-upload
          class="avatar-uploader"
          action="/api/user/avatar"
          :headers="uploadHeaders"
          :show-file-list="false"
          :before-upload="beforeAvatarUpload"
          :on-success="handleAvatarSuccess"
          :on-error="handleAvatarError"
          accept="image/*"
        >
          <el-button type="primary" size="small" class="change-avatar-btn">
            <el-icon><Camera /></el-icon>
            更换头像
          </el-button>
        </el-upload>
      </div>
      <div class="profile-info">
        <h2>{{ user?.username }}</h2>
        <p class="email">{{ user?.email }}</p>
        <p class="signature" v-if="user?.signature">{{ user.signature }}</p>
        <p class="no-signature" v-else>还没有个性签名</p>
      </div>
      <el-button @click="editDialogVisible = true">编辑资料</el-button>
    </div>
    
    <div class="profile-stats card">
      <div class="stat-item">
        <div class="stat-value">0</div>
        <div class="stat-label">发帖</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">0</div>
        <div class="stat-label">评论</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">0</div>
        <div class="stat-label">获赞</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">0</div>
        <div class="stat-label">关注</div>
      </div>
    </div>
    
    <!-- 编辑资料对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑资料" width="500px">
      <el-form :model="editForm" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="editForm.username" disabled />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="个性签名">
          <el-input
            v-model="editForm.signature"
            type="textarea"
            :rows="3"
            maxlength="100"
            show-word-limit
            placeholder="写点什么介绍自己..."
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveProfile" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import apiClient from '@/api'

export default {
  name: 'Profile',
  setup() {
    const user = ref(null)
    const editDialogVisible = ref(false)
    const saving = ref(false)
    const editForm = ref({
      username: '',
      email: '',
      signature: ''
    })
    
    const uploadHeaders = computed(() => {
      const token = localStorage.getItem('token')
      return {
        Authorization: `Bearer ${token}`
      }
    })
    
    const fetchUserInfo = async () => {
      const token = localStorage.getItem('token')
      if (!token) return
      
      try {
        const response = await apiClient.get('/api/user', {
          headers: { Authorization: `Bearer ${token}` }
        })
        user.value = response.data
        editForm.value = {
          username: response.data.username,
          email: response.data.email,
          signature: response.data.signature || ''
        }
      } catch (error) {
        console.error('获取用户信息失败:', error)
      }
    }
    
    const beforeAvatarUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt2M = file.size / 1024 / 1024 < 2
      
      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt2M) {
        ElMessage.error('图片大小不能超过 2MB!')
        return false
      }
      return true
    }
    
    const handleAvatarSuccess = (response) => {
      ElMessage.success('头像上传成功')
      fetchUserInfo()
    }
    
    const handleAvatarError = () => {
      ElMessage.error('头像上传失败')
    }
    
    const saveProfile = async () => {
      saving.value = true
      // 这里可以实现保存逻辑
      setTimeout(() => {
        saving.value = false
        editDialogVisible.value = false
        ElMessage.success('保存成功')
        fetchUserInfo()
      }, 500)
    }
    
    onMounted(() => {
      fetchUserInfo()
    })
    
    return {
      user,
      editDialogVisible,
      saving,
      editForm,
      uploadHeaders,
      beforeAvatarUpload,
      handleAvatarSuccess,
      handleAvatarError,
      saveProfile
    }
  }
}
</script>

<style scoped>
.profile-page {
  max-width: 800px;
  margin: 0 auto;
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 24px;
  margin-bottom: 20px;
}

.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.avatar-uploader {
  display: flex;
  justify-content: center;
}

.change-avatar-btn {
  font-size: 12px;
}

.profile-info {
  flex: 1;
}

.profile-info h2 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.email {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.signature {
  color: #999;
  font-size: 14px;
}

.no-signature {
  color: #ccc;
  font-size: 14px;
  font-style: italic;
}

.profile-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  text-align: center;
}

.stat-item {
  padding: 16px;
}

.stat-value {
  font-size: 28px;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 4px;
}

.stat-label {
  font-size: 14px;
  color: #999;
}
</style>
