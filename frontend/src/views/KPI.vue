<template>
  <LayoutCenter>
    <h1 class="title">维修工 KPI</h1>

    <div v-if="loading" class="tip">加载中…</div>

    <ul v-else class="list">
      <li v-for="item in kpi" :key="item.worker_id" class="item">
        <span>{{ item.name }}</span>
        <span>平均分：{{ item.avg_score.toFixed(1) }}</span>
        <span>工单数：{{ item.total }}</span>
      </li>
    </ul>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import LayoutCenter from '@/components/LayoutCenter.vue'

const kpi = ref<any[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:8000/kpi')
    kpi.value = await res.json()
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.title {
  font-size: 36px;
  font-weight: 700;
  margin-bottom: 32px;
  color: #303133;
  text-align: center;
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
