<template>
  <div class="board-page">
    <div class="board-header card">
      <div class="board-info">
        <div class="board-icon-large">
          <el-icon size="48">
            <component :is="getIcon(board?.icon)" />
          </el-icon>
        </div>
        <div class="board-title-section">
          <h1>{{ board?.name }}</h1>
          <p>{{ board?.description }}</p>
        </div>
      </div>
      <el-button type="primary" @click="$router.push('/create')">
        <el-icon><Plus /></el-icon>
        发帖
      </el-button>
    </div>
    
    <div class="posts-section">
      <div class="section-header">
        <h2>帖子列表</h2>
        <el-radio-group v-model="sortBy" size="small">
          <el-radio-button label="new">最新</el-radio-button>
          <el-radio-button label="hot">热门</el-radio-button>
        </el-radio-group>
      </div>
      
      <div class="posts-list">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
      
      <div class="pagination" v-if="total > perPage">
        <el-pagination
          v-model:current-page="page"
          :page-size="perPage"
          :total="total"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import axios from 'axios'
import PostCard from '../components/PostCard.vue'
import { School, Reading, UserFilled, Goods, Briefcase, StarFilled } from '@element-plus/icons-vue'

export default {
  name: 'Board',
  components: {
    PostCard
  },
  setup() {
    const route = useRoute()
    const board = ref(null)
    const posts = ref([])
    const page = ref(1)
    const perPage = ref(20)
    const total = ref(0)
    const sortBy = ref('new')
    
    const iconMap = {
      'school': School,
      'book': Reading,
      'users': UserFilled,
      'shopping': Goods,
      'briefcase': Briefcase,
      'heart': StarFilled
    }
    
    const getIcon = (iconName) => {
      return iconMap[iconName] || School
    }
    
    const fetchBoard = async () => {
      try {
        const response = await axios.get('/api/boards')
        board.value = response.data.find(b => b.id === parseInt(route.params.id))
      } catch (error) {
        console.error('获取板块信息失败:', error)
      }
    }
    
    const fetchPosts = async () => {
      try {
        const response = await axios.get('/api/posts', {
          params: {
            board_id: route.params.id,
            page: page.value,
            per_page: perPage.value
          }
        })
        posts.value = response.data.posts
        total.value = response.data.total
      } catch (error) {
        console.error('获取帖子失败:', error)
      }
    }
    
    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchPosts()
      window.scrollTo(0, 0)
    }
    
    watch(() => route.params.id, () => {
      fetchBoard()
      fetchPosts()
    })
    
    onMounted(() => {
      fetchBoard()
      fetchPosts()
    })
    
    return {
      board,
      posts,
      page,
      perPage,
      total,
      sortBy,
      getIcon,
      handlePageChange
    }
  }
}
</script>

<style scoped>
.board-page {
  max-width: 1000px;
  margin: 0 auto;
}

.board-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.board-info {
  display: flex;
  align-items: center;
  gap: 20px;
}

.board-icon-large {
  width: 80px;
  height: 80px;
  border-radius: 16px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.board-title-section h1 {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
}

.board-title-section p {
  color: #666;
  font-size: 14px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header h2 {
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 0;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}
</style>