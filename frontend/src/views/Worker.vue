<template>
  <LayoutCenter>
    <h1 class="title">维修工工作台</h1>

    <button @click="loadOrders" :disabled="loading" class="refresh">
      {{ loading ? '加载中…' : '刷新工单' }}
    </button>

    <ul v-if="orders.length" class="list">
      <li v-for="o in orders" :key="o.id" class="item">
        <span>#{{ o.id }} {{ o.description }}</span>
        <span>{{ o.status }}</span>
        <button
          v-if="o.status === 'pending'"
          @click="take(o.id)"
        >接单</button>
        <button
          v-if="o.status === 'processing'"
          @click="finish(o.id)"
        >完工并复制评价链接</button>
      </li>
    </ul>

    <div v-if="link" class="link-box">
      <p>已完工！评价链接：</p>
      <input readonly :value="link" />
      <button @click="copyLink">复制</button>
    </div>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useWorkerStore } from '@/stores/worker'
import LayoutCenter from '@/components/LayoutCenter.vue'

const workerStore = useWorkerStore()
const orders  = ref<any[]>([])
const loading = ref(false)
const link    = ref('')

onMounted(loadOrders)

async function loadOrders() {
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/orders')
    orders.value = await res.json()
  } catch {
    alert('网络异常')
  } finally {
    loading.value = false
  }
}

async function take(id: number) {
  await fetch(`http://127.0.0.1:8000/orders/${id}/take`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ worker_id: workerStore.id })
  })
  await loadOrders()
}

async function finish(id: number) {
  await fetch(`http://127.0.0.1:8000/orders/${id}/finish`, { method: 'PATCH' })
  await loadOrders()
  link.value = `${location.origin}/rate/${id}`
}

async function copyLink() {
  await navigator.clipboard.writeText(link.value)
  alert('评价链接已复制！')
}
</script>

<style scoped>
.title {
  font-size: 36px;
  margin-bottom: 24px;
  color: #303133;
  text-align: center;
}
.refresh {
  margin-bottom: 20px;
  padding: 8px 20px;
}
.list {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}
.link-box {
  margin-top: 20px;
  text-align: center;
}
.link-box input {
  width: 100%;
  max-width: 400px;
  margin: 8px 0;
}
</style>
