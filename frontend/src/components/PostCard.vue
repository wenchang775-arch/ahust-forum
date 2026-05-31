<template>
  <div class="post-card" :class="{ 'is-pinned': post.is_pinned, 'is-essence': post.is_essence }">
    <div class="post-header">
      <div class="post-tags">
        <el-tag v-if="post.is_pinned" type="danger" size="small" effect="dark">
          <el-icon><Top /></el-icon>
          置顶
        </el-tag>
        <el-tag v-if="post.is_essence" type="warning" size="small" effect="dark">
          <el-icon><Star /></el-icon>
          精华
        </el-tag>
        <el-tag type="info" size="small">{{ post.board_name }}</el-tag>
      </div>
      <span class="post-time">{{ formatTime(post.created_at) }}</span>
    </div>
    
    <router-link :to="`/post/${post.id}`" class="post-title">
      {{ post.title }}
    </router-link>
    
    <p class="post-content">{{ post.content }}</p>
    
    <div class="post-footer">
      <div class="post-author">
        <el-avatar :size="28" :src="post.avatar || ''">
          <el-icon><User /></el-icon>
        </el-avatar>
        <span class="author-name">{{ post.username }}</span>
      </div>
      
      <div class="post-stats">
        <span class="stat-item">
          <el-icon><View /></el-icon>
          {{ post.view_count }}
        </span>
        <span class="stat-item">
          <el-icon><ChatDotRound /></el-icon>
          {{ post.comment_count }}
        </span>
        <span class="stat-item">
          <el-icon><Pointer /></el-icon>
          {{ post.like_count }}
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PostCard',
  props: {
    post: {
      type: Object,
      required: true
    }
  },
  setup() {
    const formatTime = (time) => {
      const date = new Date(time)
      const now = new Date()
      const diff = now - date
      
      if (diff < 60000) return '刚刚'
      if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
      if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
      if (diff < 604800000) return `${Math.floor(diff / 86400000)}天前`
      
      return date.toLocaleDateString('zh-CN')
    }
    
    return { formatTime }
  }
}
</script>

<style scoped>
.post-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  border: 2px solid transparent;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
}

.post-card.is-pinned {
  border-color: #f56c6c;
  background: linear-gradient(to right, #fff5f5, white);
}

.post-card.is-essence {
  border-color: #e6a23c;
  background: linear-gradient(to right, #fdf6ec, white);
}

.post-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.post-tags {
  display: flex;
  gap: 8px;
}

.post-time {
  font-size: 13px;
  color: #999;
}

.post-title {
  font-size: 18px;
  font-weight: 600;
  color: #333;
  text-decoration: none;
  display: block;
  margin-bottom: 10px;
  line-height: 1.4;
}

.post-title:hover {
  color: #667eea;
}

.post-content {
  font-size: 14px;
  color: #666;
  line-height: 1.6;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid #f0f0f0;
}

.post-author {
  display: flex;
  align-items: center;
  gap: 8px;
}

.author-name {
  font-size: 14px;
  color: #666;
}

.post-stats {
  display: flex;
  gap: 16px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: #999;
}

.stat-item .el-icon {
  font-size: 16px;
}
</style>