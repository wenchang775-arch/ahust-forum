<template>
  <div class="create-post-page">
    <div class="card">
      <h2 class="page-title">
        <el-icon><EditPen /></el-icon>
        发布新帖
      </h2>
      
      <el-form :model="form" :rules="rules" ref="formRef">
        <el-form-item prop="board_id">
          <el-select v-model="form.board_id" placeholder="选择板块" size="large" style="width: 100%">
            <el-option
              v-for="board in boards"
              :key="board.id"
              :label="board.name"
              :value="board.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入标题"
            size="large"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item prop="content">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="10"
            placeholder="请输入内容..."
            maxlength="5000"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="上传图片">
          <ImageUploader
            ref="imageUploaderRef"
            :limit="9"
            :multiple="true"
            @images-change="handleImagesChange"
          />
        </el-form-item>
        
        <el-form-item>
          <div class="form-actions">
            <el-button @click="$router.back()">取消</el-button>
            <el-button type="primary" :loading="loading" @click="handleSubmit">
              发布
            </el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import apiClient from '@/api'
import ImageUploader from '../components/ImageUploader.vue'

export default {
  name: 'CreatePost',
  components: {
    ImageUploader
  },
  setup() {
    const router = useRouter()
    const formRef = ref(null)
    const imageUploaderRef = ref(null)
    const loading = ref(false)
    const boards = ref([])
    const uploadedImages = ref([])
    
    const form = reactive({
      board_id: null,
      title: '',
      content: ''
    })
    
    const rules = {
      board_id: [
        { required: true, message: '请选择板块', trigger: 'change' }
      ],
      title: [
        { required: true, message: '请输入标题', trigger: 'blur' },
        { min: 5, max: 100, message: '标题长度在 5 到 100 个字符', trigger: 'blur' }
      ],
      content: [
        { required: true, message: '请输入内容', trigger: 'blur' },
        { min: 10, message: '内容至少10个字符', trigger: 'blur' }
      ]
    }
    
    const fetchBoards = async () => {
      try {
        const response = await apiClient.get('/api/boards')
        boards.value = response.data
      } catch (error) {
        console.error('获取板块失败:', error)
      }
    }
    
    const handleImagesChange = (images) => {
      uploadedImages.value = images
    }
    
    const handleSubmit = async () => {
      const valid = await formRef.value.validate().catch(() => false)
      if (!valid) return
      
      loading.value = true
      try {
        // 收集已上传图片的ID
        const imageIds = uploadedImages.value.map(img => img.id).filter(Boolean)
        
        // 创建帖子（包含图片关联）
        const postData = { ...form }
        if (imageIds.length > 0) {
          postData.image_ids = imageIds
        }
        
        const postResponse = await apiClient.post('/api/posts', postData)
        const postId = postResponse.data.id
        
        ElMessage.success('发布成功')
        router.push(`/post/${postId}`)
      } catch (error) {
        ElMessage.error(error.response?.data?.error || '发布失败')
      } finally {
        loading.value = false
      }
    }
    
    onMounted(() => {
      fetchBoards()
    })
    
    return {
      form,
      formRef,
      imageUploaderRef,
      rules,
      loading,
      boards,
      handleImagesChange,
      handleSubmit
    }
  }
}
</script>

<style scoped>
.create-post-page {
  max-width: 800px;
  margin: 0 auto;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}
</style>
