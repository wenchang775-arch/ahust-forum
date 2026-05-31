<template>
  <div class="home">
    <!-- 欢迎横幅 -->
    <div class="welcome-banner">
      <div class="banner-content">
        <h1>欢迎来到安徽理工大学贴吧</h1>
        <p>校园生活、学习交流、社团活动，一切尽在掌握</p>
        <el-button type="primary" size="large" @click="$router.push('/create')" v-if="isLoggedIn">
          <el-icon><Edit /></el-icon>
          发布新帖
        </el-button>
        <el-button type="primary" size="large" @click="$router.push('/login')" v-else>
          <el-icon><User /></el-icon>
          立即加入
        </el-button>
      </div>
    </div>
    
    <!-- 板块列表 -->
    <div class="section">
      <h2 class="section-title">
        <el-icon><Grid /></el-icon>
        热门板块
      </h2>
      <div class="boards-grid">
        <BoardCard v-for="board in boards" :key="board.id" :board="board" />
      </div>
    </div>
    
    <!-- 最新帖子 -->
    <div class="section">
      <h2 class="section-title">
        <el-icon><ChatDotRound /></el-icon>
        最新帖子
      </h2>
      <div class="posts-list">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
      <div class="load-more" v-if="posts.length >= 20">
        <el-button @click="loadMore" :loading="loading">加载更多</el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import axios from 'axios'
import BoardCard from '../components/BoardCard.vue'
import PostCard from '../components/PostCard.vue'

export default {
  name: 'Home',
  components: {
    BoardCard,
    PostCard
  },
  setup() {
    const boards = ref([])
    const posts = ref([])
    const loading = ref(false)
    const page = ref(1)
    
    const isLoggedIn = computed(() => {
      return !!localStorage.getItem('token')
    })
    
    const fetchBoards = async () => {
      try {
        const response = await axios.get('/api/boards')
        boards.value = response.data
      } catch (error) {
        console.error('获取板块失败:', error)
      }
    }
    
    const fetchPosts = async () => {
      try {
        const response = await axios.get('/api/posts', {
          params: { page: page.value, per_page: 20 }
        })
        posts.value = response.data.posts
      } catch (error) {
        console.error('获取帖子失败:', error)
      }
    }
    
    const loadMore = async () => {
      loading.value = true
      page.value++
      try {
        const response = await axios.get('/api/posts', {
          params: { page: page.value, per_page: 20 }
        })
        posts.value.push(...response.data.posts)
      } catch (error) {
        console.error('加载更多失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchBoards()
      fetchPosts()
    })
    
    return {
      boards,
      posts,
      loading,
      isLoggedIn,
      loadMore
    }
  }
}
</script>

<style scoped>
.home {
  padding-bottom: 40px;
}

.welcome-banner {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  padding: 60px 40px;
  margin-bottom: 40px;
  color: white;
  text-align: center;
}

.banner-content h1 {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 16px;
}

.banner-content p {
  font-size: 18px;
  margin-bottom: 24px;
  opacity: 0.9;
}

.section {
  margin-bottom: 40px;
}

.section-title {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.section-title .el-icon {
  color: #667eea;
}

.boards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.load-more {
  text-align: center;
  margin-top: 20px;
}
</style>