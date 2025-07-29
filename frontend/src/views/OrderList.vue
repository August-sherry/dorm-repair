<template>
  <div class="fullscreen">
    <h1 class="title">工单列表</h1>

    <div v-if="loading" class="tip">加载中…</div>

    <ul v-else class="list">
      <li v-for="o in orders" :key="o.id" class="item">
        <span>{{ o.description }}</span>
        <span>优先级：{{ o.priority }}</span>
        <span>状态：{{ o.status }}</span>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const orders  = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/orders')
    orders.value = await res.json()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
/* 占满视口并居中 */
.fullscreen {
  min-height: 100vh;
  width: 100vw;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  background: #f5f7fa;
  padding: 2rem 1rem;
  box-sizing: border-box;
}


.title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 32px;
  color: #303133;
}

.tip {
  font-size: 18px;
  color: #909399;
}

.list {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.item {
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: flex;
  justify-content: space-between;
  color: #606266;
}
</style>
