<template>
  <div class="search-page">
    <div class="search-header card">
      <h2 class="page-title">
        <el-icon><Search /></el-icon>
        搜索结果
      </h2>
      <el-input
        v-model="keyword"
        placeholder="搜索帖子..."
        size="large"
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </div>
    
    <div v-if="loading" class="loading">
      <el-skeleton :rows="5" animated />
    </div>
    
    <template v-else>
      <div v-if="posts.length > 0" class="search-results">
        <div class="results-count">找到 {{ total }} 条相关结果</div>
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
      
      <div v-else-if="searched" class="empty-state card">
        <el-icon><Search /></el-icon>
        <p>未找到相关帖子</p>
        <p class="tip">试试其他关键词</p>
      </div>
    </template>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import apiClient from '@/api'
import PostCard from '../components/PostCard.vue'

export default {
  name: 'Search',
  components: {
    PostCard
  },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const keyword = ref('')
    const posts = ref([])
    const page = ref(1)
    const perPage = ref(20)
    const total = ref(0)
    const loading = ref(false)
    const searched = ref(false)
    
    const fetchResults = async () => {
      if (!keyword.value.trim()) return
      
      loading.value = true
      try {
        const response = await apiClient.get('/api/search', {
          params: {
            q: keyword.value,
            page: page.value,
            per_page: perPage.value
          }
        })
        posts.value = response.data.posts
        total.value = response.data.total
        searched.value = true
      } catch (error) {
        console.error('搜索失败:', error)
      } finally {
        loading.value = false
      }
    }
    
    const handleSearch = () => {
      if (!keyword.value.trim()) return
      page.value = 1
      router.push(`/search?q=${encodeURIComponent(keyword.value)}`)
      fetchResults()
    }
    
    const handlePageChange = (newPage) => {
      page.value = newPage
      fetchResults()
      window.scrollTo(0, 0)
    }
    
    watch(() => route.query.q, (newQuery) => {
      if (newQuery) {
        keyword.value = newQuery
        fetchResults()
      }
    })
    
    onMounted(() => {
      if (route.query.q) {
        keyword.value = route.query.q
        fetchResults()
      }
    })
    
    return {
      keyword,
      posts,
      page,
      perPage,
      total,
      loading,
      searched,
      handleSearch,
      handlePageChange
    }
  }
}
</script>

<style scoped>
.search-page {
  max-width: 1000px;
  margin: 0 auto;
}

.search-header {
  margin-bottom: 20px;
}

.search-header .el-input {
  margin-top: 16px;
}

.loading {
  padding: 40px;
}

.results-count {
  color: #666;
  font-size: 14px;
  margin-bottom: 16px;
  padding: 0 8px;
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

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.empty-state .el-icon {
  font-size: 64px;
  color: #ddd;
  margin-bottom: 20px;
}

.empty-state p {
  color: #666;
  font-size: 16px;
}

.empty-state .tip {
  color: #999;
  font-size: 14px;
  margin-top: 8px;
}
</style>