<template>
  <div class="post-detail-page">
    <div v-if="loading" class="loading">
      <el-skeleton :rows="10" animated />
    </div>
    
    <template v-else-if="post">
      <!-- 帖子内容 -->
      <div class="card post-content-card">
        <div class="post-header">
          <div class="post-tags">
            <el-tag v-if="post.is_pinned" type="danger" effect="dark">置顶</el-tag>
            <el-tag v-if="post.is_essence" type="warning" effect="dark">精华</el-tag>
            <el-tag type="info">{{ post.board_name }}</el-tag>
          </div>
          <span class="post-time">{{ formatTime(post.created_at) }}</span>
        </div>
        
        <h1 class="post-title">{{ post.title }}</h1>
        
        <div class="post-author-info">
          <el-avatar :size="48" :src="post.avatar || ''">
            <el-icon><User /></el-icon>
          </el-avatar>
          <div class="author-meta">
            <span class="author-name">{{ post.username }}</span>
            <span class="author-signature" v-if="post.signature">{{ post.signature }}</span>
          </div>
        </div>
        
        <div class="post-body">
          {{ post.content }}
        </div>
        
        <!-- 帖子图片 -->
        <div v-if="postImages.length > 0" class="post-images">
          <el-image
            v-for="img in postImages"
            :key="img.id"
            :src="img.url"
            :preview-src-list="postImages.map(i => i.url)"
            fit="cover"
            class="post-image"
          />
        </div>
        
        <div class="post-actions">
          <el-button @click="handleLike" :type="isLiked ? 'danger' : 'default'">
            <el-icon><Pointer /></el-icon>
            {{ post.like_count }} 点赞
          </el-button>
          <el-button>
            <el-icon><Share /></el-icon>
            分享
          </el-button>
        </div>
        
        <div class="post-stats-bar">
          <span><el-icon><View /></el-icon> {{ post.view_count }} 浏览</span>
          <span><el-icon><ChatDotRound /></el-icon> {{ post.comment_count }} 评论</span>
        </div>
      </div>
      
      <!-- 评论区 -->
      <div class="card comments-section">
        <h3 class="section-title">
          <el-icon><ChatDotRound /></el-icon>
          评论 ({{ post.comment_count }})
        </h3>
        
        <!-- 发表评论 -->
        <div class="comment-form" v-if="isLoggedIn">
          <el-input
            v-model="newComment"
            type="textarea"
            :rows="3"
            placeholder="写下你的评论..."
            maxlength="500"
            show-word-limit
          />
          <el-button type="primary" @click="submitComment" :loading="submitting">
            发表评论
          </el-button>
        </div>
        <div v-else class="login-tip">
          <router-link to="/login">登录</router-link> 后发表评论
        </div>
        
        <!-- 评论列表 -->
        <div class="comments-list">
          <div v-for="comment in post.comments" :key="comment.id" class="comment-item">
            <div class="comment-header">
              <el-avatar :size="36" :src="comment.avatar || ''">
                <el-icon><User /></el-icon>
              </el-avatar>
              <div class="comment-meta">
                <span class="comment-author">{{ comment.username }}</span>
                <span class="comment-time">{{ formatTime(comment.created_at) }}</span>
              </div>
            </div>
            <div class="comment-content">{{ comment.content }}</div>
            <div class="comment-actions">
              <span class="action-btn">
                <el-icon><Pointer /></el-icon>
                {{ comment.like_count }}
              </span>
              <span class="action-btn" @click="replyTo(comment)">回复</span>
            </div>
            
            <!-- 回复列表 -->
            <div v-if="comment.replies && comment.replies.length > 0" class="replies-list">
              <div v-for="reply in comment.replies" :key="reply.id" class="reply-item">
                <el-avatar :size="28" :src="reply.avatar || ''">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <div class="reply-content">
                  <span class="reply-author">{{ reply.username }}</span>
                  <span>{{ reply.content }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
    
    <div v-else class="empty-state">
      <el-icon><DocumentDelete /></el-icon>
      <p>帖子不存在或已被删除</p>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import apiClient from '@/api'

export default {
  name: 'PostDetail',
  setup() {
    const route = useRoute()
    const post = ref(null)
    const loading = ref(true)
    const newComment = ref('')
    const submitting = ref(false)
    const isLiked = ref(false)
    const postImages = ref([])
    
    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('token')
    })
    
    const fetchPost = async () => {
      try {
        const response = await apiClient.get(`/api/posts/${route.params.id}`)
        post.value = response.data
        // 获取帖子图片
        await fetchPostImages()
      } catch (error) {
        console.error('获取帖子失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const fetchPostImages = async () => {
      try {
        const response = await apiClient.get(`/api/posts/${route.params.id}/images`)
        postImages.value = response.data
      } catch (error) {
        console.error('获取帖子图片失败:', error)
      }
    }
    
    const formatTime = (time) => {
      const date = new Date(time)
      return date.toLocaleString('zh-CN')
    }
    
    const handleLike = async () => {
      if (!isLoggedIn.value) {
        ElMessage.warning('请先登录')
        return
      }
      
      try {
        const token = localStorage.getItem('token')
        await apiClient.post(`/api/posts/${post.value.id}/like`, {}, {
          headers: { Authorization: `Bearer ${token}` }
        })
        post.value.like_count++
        isLiked.value = true
        ElMessage.success('点赞成功')
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '点赞失败')
      }
    }
    
    const submitComment = async () => {
      if (!newComment.value.trim()) {
        ElMessage.warning('请输入评论内容')
        return
      }
      
      submitting.value = true
      try {
        const token = localStorage.getItem('token')
        await apiClient.post(`/api/posts/${post.value.id}/comments`, {
          content: newComment.value
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
        newComment.value = ''
        ElMessage.success('评论成功')
        fetchPost()
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '评论失败')
      } finally {
        submitting.value = false
      }
    }
    
    const replyTo = (comment) => {
      newComment.value = `@${comment.username} `
    }
    
    onMounted(() => {
      fetchPost()
    })
    
    return {
      post,
      postImages,
      loading,
      newComment,
      submitting,
      isLiked,
      isLoggedIn,
      formatTime,
      handleLike,
      submitComment,
      replyTo
    }
  }
}
</script>

<style scoped>
.post-detail-page {
  max-width: 900px;
  margin: 0 auto;
}

.loading {
  padding: 40px;
}

.post-content-card {
  margin-bottom: 20px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.post-tags {
  display: flex;
  gap: 8px;
}

.post-time {
  font-size: 14px;
  color: #999;
}

.post-title {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  line-height: 1.4;
}

.post-author-info {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 20px;
}

.author-meta {
  display: flex;
  flex-direction: column;
}

.author-name {
  font-weight: 600;
  color: #333;
}

.author-signature {
  font-size: 13px;
  color: #999;
}

.post-body {
  font-size: 16px;
  line-height: 1.8;
  color: #333;
  white-space: pre-wrap;
  margin-bottom: 24px;
}

.post-images {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 12px;
  margin-bottom: 24px;
}

.post-image {
  width: 100%;
  height: 200px;
  border-radius: 8px;
  cursor: pointer;
}

.post-actions {
  display: flex;
  gap: 12px;
  margin-bottom: 16px;
}

.post-stats-bar {
  display: flex;
  gap: 24px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
  color: #999;
  font-size: 14px;
}

.post-stats-bar span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.comments-section {
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.comment-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
  margin-bottom: 24px;
}

.comment-form .el-button {
  align-self: flex-end;
}

.login-tip {
  text-align: center;
  padding: 20px;
  color: #999;
  background: #f8f9fa;
  border-radius: 8px;
  margin-bottom: 24px;
}

.login-tip a {
  color: #667eea;
  text-decoration: none;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  padding-bottom: 20px;
  border-bottom: 1px solid #f0f0f0;
}

.comment-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
}

.comment-meta {
  display: flex;
  flex-direction: column;
}

.comment-author {
  font-weight: 600;
  color: #333;
}

.comment-time {
  font-size: 13px;
  color: #999;
}

.comment-content {
  font-size: 15px;
  line-height: 1.6;
  color: #333;
  margin-bottom: 12px;
  padding-left: 48px;
}

.comment-actions {
  display: flex;
  gap: 16px;
  padding-left: 48px;
}

.action-btn {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #999;
  font-size: 13px;
  cursor: pointer;
}

.action-btn:hover {
  color: #667eea;
}

.replies-list {
  margin-top: 12px;
  margin-left: 48px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
}

.reply-item {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 0;
}

.reply-content {
  font-size: 14px;
  line-height: 1.5;
}

.reply-author {
  font-weight: 600;
  color: #667eea;
  margin-right: 8px;
}
</style>