<template>
  <LayoutCenter>
    <h1 class="title">维修工登录</h1>

    <form @submit.prevent="handleLogin" class="form">
      <label>
        <span>工号</span>
        <input v-model="id" type="number" required />
      </label>

      <label>
        <span>手机号</span>
        <input v-model="phone" type="tel" required />
      </label>

      <button type="submit" :disabled="loading" class="submit-btn">
        {{ loading ? '登录中…' : '登录' }}
      </button>

      <p v-if="error" class="error">{{ error }}</p>
    </form>
  </LayoutCenter>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useWorkerStore } from '@/stores/worker'
import LayoutCenter from '@/components/LayoutCenter.vue'

const id     = ref('')
const phone  = ref('')
const error  = ref('')
const loading = ref(false)
const router  = useRouter()
const workerStore = useWorkerStore()

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const res = await fetch('http://127.0.0.1:8000/worker/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ id: Number(id.value), phone: phone.value.trim() })
    })
    const data = await res.json()
    if (!res.ok) {
      error.value = data.detail || '登录失败'
      return
    }
  workerStore.login(data.id, data.phone)
  router.replace('/admin/worker')
  } catch {
    error.value = '网络异常'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.title {
  font-size: 42px;
  font-weight: 700;
  margin-bottom: 40px;
  color: #303133;
  text-align: center;
}
.form {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 24px;
  font-size: 20px;
}
.form input {
  width: 100%;
  padding: 12px;
  font-size: 20px;
  border-radius: 8px;
  border: 1px solid #dcdfe6;
}
.submit-btn {
  padding: 14px 0;
  font-size: 22px;
  border-radius: 8px;
  background: #409eff;
  color: #fff;
  border: none;
  cursor: pointer;
}
.error {
  color: crimson;
  text-align: center;
  margin-top: 12px;
}
</style>
