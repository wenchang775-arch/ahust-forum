<template>
  <router-link :to="`/board/${board.id}`" class="board-card">
    <div class="board-icon">
      <el-icon size="32">
        <component :is="getIcon(board.icon)" />
      </el-icon>
    </div>
    <div class="board-info">
      <h3 class="board-name">{{ board.name }}</h3>
      <p class="board-desc">{{ board.description }}</p>
    </div>
    <el-icon class="arrow-icon"><ArrowRight /></el-icon>
  </router-link>
</template>

<script>
import { School, Reading, UserFilled, Goods, Briefcase, StarFilled } from '@element-plus/icons-vue'

export default {
  name: 'BoardCard',
  props: {
    board: {
      type: Object,
      required: true
    }
  },
  setup() {
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
    
    return { getIcon }
  }
}
</script>

<style scoped>
.board-card {
  display: flex;
  align-items: center;
  gap: 16px;
  background: white;
  border-radius: 12px;
  padding: 20px;
  text-decoration: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
}

.board-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.board-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  flex-shrink: 0;
}

.board-info {
  flex: 1;
}

.board-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 4px;
}

.board-desc {
  font-size: 13px;
  color: #999;
  line-height: 1.4;
}

.arrow-icon {
  color: #ccc;
  font-size: 20px;
}

.board-card:hover .arrow-icon {
  color: #667eea;
}
</style>