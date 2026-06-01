<template>
  <div class="image-uploader">
    <el-upload
      :action="uploadUrl"
      :headers="uploadHeaders"
      :before-upload="beforeUpload"
      :on-success="handleSuccess"
      :on-error="handleError"
      :on-remove="handleRemove"
      :file-list="fileList"
      list-type="picture-card"
      :limit="limit"
      :multiple="multiple"
      accept="image/*"
    >
      <el-icon><Plus /></el-icon>
      <template #tip>
        <div class="el-upload__tip">
          支持 JPG/PNG/GIF/WEBP 格式，单张不超过 5MB
        </div>
      </template>
    </el-upload>
  </div>
</template>

<script>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'

export default {
  name: 'ImageUploader',
  props: {
    limit: {
      type: Number,
      default: 9
    },
    multiple: {
      type: Boolean,
      default: true
    },
    postId: {
      type: Number,
      default: null
    }
  },
  emits: ['upload-success', 'upload-error', 'images-change'],
  setup(props, { emit }) {
    const fileList = ref([])
    const uploadedImages = ref([])
    
    const uploadUrl = computed(() => {
      const apiUrl = process.env.VUE_APP_API_URL || ''
      return `${apiUrl}/api/upload`
    })
    
    const uploadHeaders = computed(() => {
      const token = localStorage.getItem('token')
      return {
        Authorization: `Bearer ${token}`
      }
    })
    
    const beforeUpload = (file) => {
      const isImage = file.type.startsWith('image/')
      const isLt5M = file.size / 1024 / 1024 < 5
      
      if (!isImage) {
        ElMessage.error('只能上传图片文件!')
        return false
      }
      if (!isLt5M) {
        ElMessage.error('图片大小不能超过 5MB!')
        return false
      }
      return true
    }
    
    const handleSuccess = (response, file) => {
      uploadedImages.value.push(response)
      emit('upload-success', response)
      emit('images-change', uploadedImages.value)
      ElMessage.success('图片上传成功')
    }
    
    const handleError = (error, file) => {
      ElMessage.error('图片上传失败')
      emit('upload-error', error)
    }
    
    const handleRemove = (file, fileList) => {
      const index = uploadedImages.value.findIndex(img => img.url === file.url)
      if (index > -1) {
        uploadedImages.value.splice(index, 1)
      }
      emit('images-change', uploadedImages.value)
    }
    
    const clearImages = () => {
      fileList.value = []
      uploadedImages.value = []
      emit('images-change', [])
    }
    
    return {
      fileList,
      uploadUrl,
      uploadHeaders,
      beforeUpload,
      handleSuccess,
      handleError,
      handleRemove,
      clearImages,
      uploadedImages
    }
  }
}
</script>

<style scoped>
.image-uploader {
  margin: 16px 0;
}

:deep(.el-upload--picture-card) {
  width: 100px;
  height: 100px;
  line-height: 100px;
}

:deep(.el-upload-list--picture-card .el-upload-list__item) {
  width: 100px;
  height: 100px;
}
</style>
